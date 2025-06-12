#!/usr/bin/env python3
"""
Entry point for AWS Elastic Beanstalk deployment
"""

from api import app

# Elastic Beanstalk looks for 'application' by default
application = app

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(application, host="0.0.0.0", port=port)