#!/usr/bin/env python3
"""
Tests for AdSense integration in MedSim
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app
import sys
sys.path.append('..')
from api import app
from config import Config

client = TestClient(app)


def test_adsense_config_endpoint_no_env():
    """Test AdSense config endpoint when no environment variables are set."""
    with patch.object(Config, 'adsense_client_id', ''):
        with patch.object(Config, 'adsense_slot_id', ''):
            response = client.get("/api/config/adsense")
            assert response.status_code == 200
            data = response.json()
            assert data["enabled"] is False
            assert data["client_id"] is None
            assert data["slot_id"] is None


def test_adsense_config_endpoint_with_env():
    """Test AdSense config endpoint when environment variables are set."""
    with patch.object(Config, 'adsense_client_id', 'ca-pub-1234567890123456'):
        with patch.object(Config, 'adsense_slot_id', 'test-slot'):
            response = client.get("/api/config/adsense")
            assert response.status_code == 200
            data = response.json()
            assert data["enabled"] is True
            assert data["client_id"] == "ca-pub-1234567890123456"
            assert data["slot_id"] == "test-slot"


def test_log_ad_impression_no_session():
    """Test ad impression logging with invalid session."""
    response = client.post("/api/game/log-ad-impression", json={
        "session_id": "invalid-session-id",
        "ad_type": "banner",
        "placement": "bottom"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["skipped", "error"]


def test_log_ad_impression_with_metadata():
    """Test ad impression logging with metadata."""
    # First create a game session
    create_response = client.post("/api/game/create", json={
        "role": "doctor",
        "difficulty": "medium"
    })
    assert create_response.status_code == 200
    session_id = create_response.json()["session_id"]
    
    # Log ad impression
    response = client.post("/api/game/log-ad-impression", json={
        "session_id": session_id,
        "ad_type": "banner",
        "placement": "mobile-bottom",
        "metadata": {
            "viewport_width": 375,
            "viewport_height": 812
        }
    })
    assert response.status_code == 200
    data = response.json()
    # The response will vary based on session implementation
    assert "status" in data


def test_ad_impression_in_session_log():
    """Test that ad impressions are properly stored in session logs."""
    from session_logger import SessionLogger, SessionLog
    
    # Create a session logger and log
    logger = SessionLogger()
    session_log = SessionLog(
        session_id="test-session",
        start_time="2024-01-01T00:00:00",
        role="doctor"
    )
    
    # Log an ad impression
    logger.log_ad_impression(
        session_log,
        ad_type="banner",
        placement="desktop-bottom",
        metadata={"test": True}
    )
    
    # Verify the impression was logged
    assert len(session_log.ad_impressions) == 1
    impression = session_log.ad_impressions[0]
    assert impression["type"] == "banner"
    assert impression["placement"] == "desktop-bottom"
    assert impression["metadata"]["test"] is True
    assert "timestamp" in impression


# Cypress test specification (to be created as a separate file)
CYPRESS_TEST_SPEC = """
// cypress/e2e/adsense.cy.js

describe('AdSense Integration', () => {
  beforeEach(() => {
    // Set test AdSense environment variable
    cy.intercept('GET', '/api/config/adsense', {
      statusCode: 200,
      body: {
        enabled: true,
        client_id: 'ca-pub-0000000000000000',
        slot_id: 'test'
      }
    }).as('getAdConfig');
  });

  it('should load AdSense script when enabled', () => {
    cy.visit('/');
    cy.wait('@getAdConfig');
    
    // Check that AdSense script is loaded
    cy.get('script[src*="googlesyndication.com"]').should('exist');
    cy.get('script[data-ad-client="ca-pub-0000000000000000"]').should('exist');
  });

  it('should show ad container after page load', () => {
    cy.visit('/');
    cy.wait('@getAdConfig');
    
    // Wait for ad container to be visible
    cy.get('#adsense-container', { timeout: 10000 }).should('be.visible');
    cy.get('.adsbygoogle').should('exist');
  });

  it('should hide ads during modal interactions', () => {
    // Start a game
    cy.visit('/');
    cy.get('[data-role="doctor"]').click();
    cy.get('#start-doctor-game').click();
    
    // Open physical exam modal
    cy.get('#pex-btn').click();
    
    // Check that no-ads class is applied
    cy.get('.screen.active').should('have.class', 'no-ads');
    
    // Close modal
    cy.get('#close-pex-btn').click();
    
    // Check that no-ads class is removed
    cy.get('.screen.active').should('not.have.class', 'no-ads');
  });

  it('should log ad impressions when ads are shown', () => {
    cy.intercept('POST', '/api/game/log-ad-impression', {
      statusCode: 200,
      body: {
        status: 'logged',
        impression_count: 1
      }
    }).as('logAdImpression');

    // Start a game to get a session
    cy.visit('/');
    cy.get('[data-role="doctor"]').click();
    cy.get('#start-doctor-game').click();
    
    // Wait for ad impression to be logged
    cy.wait('@logAdImpression', { timeout: 10000 }).then((interception) => {
      expect(interception.request.body).to.have.property('session_id');
      expect(interception.request.body).to.have.property('ad_type', 'banner');
      expect(interception.request.body.placement).to.match(/mobile-bottom|desktop-bottom/);
    });
  });
});
"""


if __name__ == "__main__":
    # Write Cypress test file
    with open("cypress_adsense_test.js", "w") as f:
        f.write(CYPRESS_TEST_SPEC)
    print("✅ Cypress test specification written to cypress_adsense_test.js")
    
    # Run pytest
    pytest.main([__file__, "-v"])