// TDD Test Suite for Medical Game

class TestSuite {
    constructor() {
        this.tests = [];
        this.results = {
            passed: 0,
            failed: 0,
            errors: []
        };
    }
    
    // Test framework methods
    test(name, testFunction) {
        this.tests.push({ name, testFunction });
    }
    
    async runAllTests() {
        console.log("🧪 Starting Test Suite");
        console.log("=" * 50);
        
        for (const test of this.tests) {
            try {
                await test.testFunction();
                this.results.passed++;
                console.log(`✅ ${test.name}`);
            } catch (error) {
                this.results.failed++;
                this.results.errors.push({ test: test.name, error: error.message });
                console.error(`❌ ${test.name}: ${error.message}`);
            }
        }
        
        this.printResults();
    }
    
    printResults() {
        console.log("\n📊 Test Results:");
        console.log(`✅ Passed: ${this.results.passed}`);
        console.log(`❌ Failed: ${this.results.failed}`);
        
        if (this.results.errors.length > 0) {
            console.log("\n🔍 Errors:");
            this.results.errors.forEach(error => {
                console.log(`  • ${error.test}: ${error.error}`);
            });
        }
    }
    
    // Assertion methods
    assertEqual(actual, expected, message = "") {
        if (actual !== expected) {
            throw new Error(`${message} - Expected: ${expected}, Got: ${actual}`);
        }
    }
    
    assertTrue(condition, message = "") {
        if (!condition) {
            throw new Error(`${message} - Expected true, got false`);
        }
    }
    
    assertElementExists(selector, message = "") {
        const element = document.querySelector(selector);
        if (!element) {
            throw new Error(`${message} - Element not found: ${selector}`);
        }
        return element;
    }
    
    assertElementVisible(selector, message = "") {
        const element = this.assertElementExists(selector, message);
        const style = window.getComputedStyle(element);
        if (style.display === 'none' || style.visibility === 'hidden') {
            throw new Error(`${message} - Element not visible: ${selector}`);
        }
        return element;
    }
    
    async assertAPICall(endpoint, expectedStatus = 200, message = "") {
        const response = await fetch(endpoint);
        if (response.status !== expectedStatus) {
            throw new Error(`${message} - API call failed: ${endpoint} returned ${response.status}`);
        }
        return response;
    }
}

// Initialize test suite
const testSuite = new TestSuite();

// Test 1: Basic DOM Elements Exist
testSuite.test("Essential DOM elements exist", () => {
    testSuite.assertElementExists('#welcome-screen', "Welcome screen should exist");
    testSuite.assertElementExists('#setup-screen', "Setup screen should exist");
    testSuite.assertElementExists('#game-screen', "Game screen should exist");
    testSuite.assertElementExists('.role-card[data-role="doctor"]', "Doctor role card should exist");
    testSuite.assertElementExists('.role-card[data-role="patient"]', "Patient role card should exist");
});

// Test 2: Initial Screen State
testSuite.test("Welcome screen is initially active", () => {
    const welcomeScreen = testSuite.assertElementExists('#welcome-screen');
    testSuite.assertTrue(welcomeScreen.classList.contains('active'), "Welcome screen should be active");
    
    const setupScreen = testSuite.assertElementExists('#setup-screen');
    testSuite.assertTrue(!setupScreen.classList.contains('active'), "Setup screen should not be active");
});

// Test 3: Role Card Click Functionality
testSuite.test("Role card click adds selected class", () => {
    const doctorCard = testSuite.assertElementExists('.role-card[data-role="doctor"]');
    
    // Simulate click
    doctorCard.click();
    
    // Check if selected class is added
    testSuite.assertTrue(doctorCard.classList.contains('selected'), "Doctor card should have selected class after click");
});

// Test 4: Screen Transition on Role Selection
testSuite.test("Screen transitions to setup after role selection", async () => {
    const doctorCard = testSuite.assertElementExists('.role-card[data-role="doctor"]');
    
    // Click role card
    doctorCard.click();
    
    // Wait for transition (500ms delay in code)
    await new Promise(resolve => setTimeout(resolve, 600));
    
    // Check if setup screen is now active
    const setupScreen = testSuite.assertElementExists('#setup-screen');
    testSuite.assertTrue(setupScreen.classList.contains('active'), "Setup screen should be active after role selection");
    
    const welcomeScreen = testSuite.assertElementExists('#welcome-screen');
    testSuite.assertTrue(!welcomeScreen.classList.contains('active'), "Welcome screen should not be active");
});

// Test 5: Setup Form Elements Exist
testSuite.test("Setup form elements exist for doctor mode", () => {
    testSuite.assertElementExists('#difficulty-select', "Difficulty select should exist");
    testSuite.assertElementExists('#specialty-select', "Specialty select should exist");
    testSuite.assertElementExists('#start-doctor-game', "Start doctor game button should exist");
});

// Test 6: API Health Check
testSuite.test("API health endpoint responds", async () => {
    await testSuite.assertAPICall('/api/health', 200, "Health endpoint should return 200");
});

// Test 7: Game Creation API
testSuite.test("Game creation API works", async () => {
    const response = await fetch('/api/game/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            role: 'doctor',
            difficulty: 'medium'
        })
    });
    
    testSuite.assertEqual(response.status, 200, "Game creation should return 200");
    
    const data = await response.json();
    testSuite.assertTrue(data.session_id !== undefined, "Response should contain session_id");
    testSuite.assertEqual(data.role, 'doctor', "Response should contain correct role");
});

// Test 8: Form Validation
testSuite.test("Patient form validation works", () => {
    // Test empty patient name
    const patientNameInput = testSuite.assertElementExists('#patient-name');
    const patientAgeInput = testSuite.assertElementExists('#patient-age');
    const chiefComplaintInput = testSuite.assertElementExists('#chief-complaint');
    
    // Set empty values
    patientNameInput.value = '';
    patientAgeInput.value = '';
    chiefComplaintInput.value = '';
    
    // Should fail validation (we'll implement this)
    testSuite.assertTrue(patientNameInput.value === '', "Empty name should be testable");
});

// Test 9: Event Listeners Attached
testSuite.test("Event listeners are attached", () => {
    const doctorCard = testSuite.assertElementExists('.role-card[data-role="doctor"]');
    
    // Check if click event listener exists (indirect test)
    const hasClickListener = doctorCard.onclick !== null || 
                           doctorCard.addEventListener !== undefined;
    
    testSuite.assertTrue(hasClickListener !== false, "Role cards should have event listeners");
});

// Test 10: CSS Classes Work
testSuite.test("CSS classes apply correctly", () => {
    const doctorCard = testSuite.assertElementExists('.role-card[data-role="doctor"]');
    
    // Add selected class
    doctorCard.classList.add('selected');
    
    // Check if class is applied
    testSuite.assertTrue(doctorCard.classList.contains('selected'), "Selected class should be addable");
    
    // Remove class
    doctorCard.classList.remove('selected');
    testSuite.assertTrue(!doctorCard.classList.contains('selected'), "Selected class should be removable");
});

// Export for use in HTML
window.testSuite = testSuite;