// Medical Simulation Game - Frontend JavaScript

class MedicalGameApp {
    constructor() {
        this.currentSession = null;
        this.currentRole = null;
        this.isLoading = false;
        
        this.initializeElements();
        this.attachEventListeners();
        this.loadAvailableSpecialties();
        this.showScreen('welcome');
    }
    
    initializeElements() {
        // Screens
        this.screens = {
            welcome: document.getElementById('welcome-screen'),
            setup: document.getElementById('setup-screen'),
            game: document.getElementById('game-screen')
        };
        
        // Navigation
        this.navBrand = document.getElementById('nav-brand');
        this.backToWelcomeBtn = document.getElementById('back-to-welcome');
        this.endGameBtn = document.getElementById('end-game-btn');
        this.patientEndGameBtn = document.getElementById('patient-end-game-btn');
        this.languageBtn = document.getElementById('language-btn');
        
        // Role selection
        this.roleCards = document.querySelectorAll('.role-card');
        
        // Setup forms
        this.doctorSetup = document.getElementById('doctor-setup');
        this.patientSetup = document.getElementById('patient-setup');
        this.setupTitle = document.getElementById('setup-title');
        
        // Form elements
        this.difficultySelect = document.getElementById('difficulty-select');
        this.specialtySelect = document.getElementById('specialty-select');
        this.patientNameInput = document.getElementById('patient-name');
        this.patientAgeInput = document.getElementById('patient-age');
        this.patientGenderSelect = document.getElementById('patient-gender');
        this.chiefComplaintInput = document.getElementById('chief-complaint');
        this.doctorSpecialtySelect = document.getElementById('doctor-specialty');
        
        // Game buttons
        this.startDoctorGameBtn = document.getElementById('start-doctor-game');
        this.startPatientGameBtn = document.getElementById('start-patient-game');
        
        // Game interface
        this.gameTitle = document.getElementById('game-title');
        this.roleIndicator = document.getElementById('role-indicator');
        this.difficultyIndicator = document.getElementById('difficulty-indicator');
        this.specialtyIndicator = document.getElementById('specialty-indicator');
        
        // Patient info panel
        this.patientInfoPanel = document.getElementById('patient-info-panel');
        this.patientNameDisplay = document.getElementById('patient-name-display');
        this.patientAgeDisplay = document.getElementById('patient-age-display');
        this.patientGenderDisplay = document.getElementById('patient-gender-display');
        this.chiefComplaintDisplay = document.getElementById('chief-complaint-display');
        
        // Chat interface
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendMessageBtn = document.getElementById('send-message-btn');
        
        // Diagnosis panel
        this.diagnosisPanel = document.getElementById('diagnosis-panel');
        this.diagnosisInput = document.getElementById('diagnosis-input');
        this.submitDiagnosisBtn = document.getElementById('submit-diagnosis-btn');
        this.attemptsCount = document.getElementById('attempts-count');
        
        // Modal
        this.resultsModal = document.getElementById('results-modal');
        this.resultsTitle = document.getElementById('results-title');
        this.resultsContent = document.getElementById('results-content');
        this.closeModalBtn = document.getElementById('close-modal');
        this.newCaseBtn = document.getElementById('new-case-btn');
        this.backToMenuBtn = document.getElementById('back-to-menu-btn');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loading-overlay');
        
        // Quick action buttons (PEx/Lab)
        this.quickActionsDiv = document.getElementById('quick-actions');
        this.pexBtn = document.getElementById('pex-btn');
        this.labTestBtn = document.getElementById('lab-test-btn');
        this.doctorGuideText = document.getElementById('doctor-guide-text');
        
        // Patient mode elements
        this.patientChatMessages = document.getElementById('patient-chat-messages');
        this.patientMessageInput = document.getElementById('patient-message-input');
        this.patientSendBtn = document.getElementById('patient-send-btn');
        this.patientEndGameBtn = document.getElementById('patient-end-game-btn');
        
        // User info displays
        this.userNameDisplay = document.getElementById('user-name-display');
        this.userAgeDisplay = document.getElementById('user-age-display');
        this.userGenderDisplay = document.getElementById('user-gender-display');
        this.userComplaintDisplay = document.getElementById('user-complaint-display');
        this.doctorSpecialtyDisplay = document.getElementById('doctor-specialty-display');
        this.patientSpecialtyIndicator = document.getElementById('patient-specialty-indicator');
        
        // Examination modals
        this.pexModal = document.getElementById('pex-modal');
        this.labModal = document.getElementById('lab-modal');
        this.pexContent = document.getElementById('pex-content');
        this.labContent = document.getElementById('lab-content');
        this.closePexModalBtn = document.getElementById('close-pex-modal');
        this.closePexBtn = document.getElementById('close-pex-btn');
        this.closeLabModalBtn = document.getElementById('close-lab-modal');
        this.closeLabBtn = document.getElementById('close-lab-btn');
        
        // Show answer button
        this.showAnswerBtn = document.getElementById('show-answer-btn');
        
        // Show multiple choice button
        this.showMultipleChoiceBtn = document.getElementById('show-multiple-choice-btn');
        
        // Track button states
        this.pexRequested = false;
        this.labRequested = false;
    }
    
    attachEventListeners() {
        // Navigation
        if (this.navBrand) this.navBrand.addEventListener('click', () => {
            this.logButtonClick('nav-brand', 'MedSim Logo');
            this.goToWelcome();
        });
        if (this.backToWelcomeBtn) this.backToWelcomeBtn.addEventListener('click', () => {
            this.logButtonClick('back-to-welcome', 'Back');
            this.showScreen('welcome');
        });
        if (this.endGameBtn) this.endGameBtn.addEventListener('click', () => {
            this.logButtonClick('end-game-btn', 'End Session');
            this.endGame();
        });
        if (this.languageBtn) this.languageBtn.addEventListener('click', () => {
            this.logButtonClick('language-btn', 'Language');
            this.showLanguageMessage();
        });
        
        // Role selection
        if (this.roleCards) {
            this.roleCards.forEach(card => {
                card.addEventListener('click', () => this.selectRole(card.dataset.role));
            });
        }
        
        // Setup buttons
        if (this.startDoctorGameBtn) this.startDoctorGameBtn.addEventListener('click', () => this.startDoctorGame());
        if (this.startPatientGameBtn) this.startPatientGameBtn.addEventListener('click', () => this.startPatientGame());
        
        // Chat
        if (this.sendMessageBtn) this.sendMessageBtn.addEventListener('click', () => this.sendMessage());
        if (this.messageInput) {
            this.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
        
        // Diagnosis
        if (this.submitDiagnosisBtn) this.submitDiagnosisBtn.addEventListener('click', () => this.submitDiagnosis());
        if (this.diagnosisInput) {
            this.diagnosisInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.submitDiagnosis();
                }
            });
        }
        
        // Modal
        if (this.closeModalBtn) this.closeModalBtn.addEventListener('click', () => this.closeModal());
        if (this.newCaseBtn) this.newCaseBtn.addEventListener('click', () => this.startNewCase());
        if (this.backToMenuBtn) this.backToMenuBtn.addEventListener('click', () => this.backToMenu());
        
        // Click outside modal to close
        if (this.resultsModal) {
            this.resultsModal.addEventListener('click', (e) => {
                if (e.target === this.resultsModal) {
                    this.closeModal();
                }
            });
        }
        
        // Quick action buttons
        if (this.pexBtn) this.pexBtn.addEventListener('click', () => this.performPhysicalExam());
        if (this.labTestBtn) this.labTestBtn.addEventListener('click', () => this.performLabTests());
        
        // Show answer button
        if (this.showAnswerBtn) this.showAnswerBtn.addEventListener('click', () => this.showAnswer());
        
        // Show multiple choice button
        if (this.showMultipleChoiceBtn) this.showMultipleChoiceBtn.addEventListener('click', () => this.showMultipleChoice());
        
        // Examination modal close buttons
        if (this.closePexModalBtn) this.closePexModalBtn.addEventListener('click', () => this.closePexModal());
        if (this.closePexBtn) this.closePexBtn.addEventListener('click', () => this.closePexModal());
        if (this.closeLabModalBtn) this.closeLabModalBtn.addEventListener('click', () => this.closeLabModal());
        if (this.closeLabBtn) this.closeLabBtn.addEventListener('click', () => this.closeLabModal());
        
        // Click outside examination modals to close
        if (this.pexModal) {
            this.pexModal.addEventListener('click', (e) => {
                if (e.target === this.pexModal) {
                    this.closePexModal();
                }
            });
        }
        
        if (this.labModal) {
            this.labModal.addEventListener('click', (e) => {
                if (e.target === this.labModal) {
                    this.closeLabModal();
                }
            });
        }
        
        // Patient mode end game button (patient mode uses unified chat elements)
        if (this.patientEndGameBtn) this.patientEndGameBtn.addEventListener('click', () => this.endGame());
    }
    
    showScreen(screenName) {
        // Hide all screens
        Object.values(this.screens).forEach(screen => {
            screen.classList.remove('active');
        });
        
        // Show target screen
        this.screens[screenName].classList.add('active');
        
        // Reset role selection when going back to welcome
        if (screenName === 'welcome') {
            this.currentRole = null;
            this.roleCards.forEach(card => card.classList.remove('selected'));
        }
    }
    
    async loadAvailableSpecialties() {
        try {
            const response = await fetch('/api/specialties');
            const data = await response.json();
            
            if (data.specialties) {
                // Update BOTH doctor mode specialty select AND patient mode doctor specialty select
                const specialtySelects = [this.specialtySelect, this.doctorSpecialtySelect];
                
                specialtySelects.forEach(selectElement => {
                    if (selectElement) {
                        // Clear existing options
                        selectElement.innerHTML = '<option value="">Any Specialty</option>';
                        
                        // Add specialties from API
                        data.specialties.forEach(specialty => {
                            const option = document.createElement('option');
                            option.value = specialty.value;
                            option.textContent = specialty.display;
                            selectElement.appendChild(option);
                        });
                    }
                });
                
                console.log(`Loaded ${data.total} specialties from server`);
            }
        } catch (error) {
            console.error('Failed to load specialties:', error);
            // Keep the existing hardcoded specialties as fallback
        }
    }
    
    selectRole(role) {
        this.currentRole = role;
        
        // Update UI
        this.roleCards.forEach(card => {
            card.classList.toggle('selected', card.dataset.role === role);
        });
        
        // Log role selection (will only log if patient mode)
        if (role === 'patient') {
            // Note: No session yet, this is just for tracking user flow
            console.log('Patient role selected');
        }
        
        // Show setup screen after delay
        setTimeout(() => {
            this.showSetupScreen(role);
        }, 300);
    }
    
    showSetupScreen(role) {
        this.showScreen('setup');
        
        if (role === 'doctor') {
            this.setupTitle.textContent = 'Doctor Mode Setup';
            this.doctorSetup.style.display = 'block';
            this.patientSetup.style.display = 'none';
        } else {
            this.setupTitle.textContent = 'Patient Mode Setup';
            this.doctorSetup.style.display = 'none';
            this.patientSetup.style.display = 'block';
        }
    }
    
    async startDoctorGame() {
        if (this.isLoading) return;
        
        try {
            this.showLoading('Creating your clinical session...');
            
            const difficulty = this.difficultySelect.value;
            const specialty = this.specialtySelect.value === "" ? null : this.specialtySelect.value;
            
            console.log('Doctor session request:', { role: 'doctor', difficulty, specialty });
            
            // Create game session with longer timeout
            const response = await this.apiCall('/api/game/create', 'POST', {
                role: 'doctor',
                difficulty: difficulty,
                specialty: specialty
            }, 40000); // 40 second timeout for game creation
            
            this.currentSession = response.session_id;
            
            // Setup game UI
            this.setupDoctorGameUI(response);
            this.showScreen('game');
            
        } catch (error) {
            this.showError('Failed to start doctor session: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    async startPatientGame() {
        if (this.isLoading) return;
        
        // Validate form first
        if (!this.validatePatientForm()) {
            return;
        }
        
        try {
            this.showLoading('Setting up your appointment...');
            
            // First create session with longer timeout
            const sessionResponse = await this.apiCall('/api/game/create', 'POST', {
                role: 'patient',
                difficulty: 'medium'  // Default difficulty for patient mode
            }, 60000); // 60 second timeout
            
            this.currentSession = sessionResponse.session_id;
            console.log('Patient session created:', this.currentSession);
            
            // Add a small delay to ensure session is saved
            await new Promise(resolve => setTimeout(resolve, 500));
            
            // Then setup patient with longer timeout
            const setupResponse = await this.apiCall('/api/game/setup-patient', 'POST', {
                session_id: this.currentSession,
                patient_name: this.patientNameInput.value,
                patient_age: parseInt(this.patientAgeInput.value),
                patient_gender: this.patientGenderSelect.value,
                chief_complaint: this.chiefComplaintInput.value,
                specialty: this.doctorSpecialtySelect.value || ""  // Ensure empty string for "any"
            }, 60000); // 60 second timeout
            
            // Log game start
            await this.logInteraction('game_start', {
                screen: 'patient_setup',
                form_data: {
                    patient_name: this.patientNameInput.value,
                    patient_age: parseInt(this.patientAgeInput.value),
                    patient_gender: this.patientGenderSelect.value,
                    chief_complaint: this.chiefComplaintInput.value,
                    specialty: this.doctorSpecialtySelect.value
                }
            });
            
            // Setup game UI
            this.setupPatientGameUI(setupResponse);
            
        } catch (error) {
            this.showError('Failed to start patient session: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    setupDoctorGameUI(gameData) {
        // Update game header
        if (this.gameTitle) this.gameTitle.textContent = `Patient: ${gameData.patient_name}`;
        if (this.roleIndicator) this.roleIndicator.textContent = 'Doctor Mode';
        if (this.difficultyIndicator) this.difficultyIndicator.textContent = gameData.difficulty.charAt(0).toUpperCase() + gameData.difficulty.slice(1);
        if (this.specialtyIndicator) this.specialtyIndicator.textContent = gameData.specialty || 'General';
        
        // Show patient info panel
        if (this.patientInfoPanel) this.patientInfoPanel.style.display = 'block';
        if (this.patientNameDisplay) this.patientNameDisplay.textContent = gameData.patient_name;
        if (this.patientAgeDisplay) this.patientAgeDisplay.textContent = gameData.patient_age;
        if (this.patientGenderDisplay) this.patientGenderDisplay.textContent = gameData.patient_gender;
        if (this.chiefComplaintDisplay) this.chiefComplaintDisplay.textContent = gameData.chief_complaint;
        
        // Show diagnosis panel
        if (this.diagnosisPanel) this.diagnosisPanel.style.display = 'block';
        
        // Reset attempts count to 0
        if (this.attemptsCount) this.attemptsCount.textContent = '0';
        
        // Show quick actions for doctor mode but keep buttons disabled initially
        if (this.quickActionsDiv) this.quickActionsDiv.style.display = 'flex';
        if (this.doctorGuideText) this.doctorGuideText.style.display = 'flex';
        this.resetQuickActionButtons();
        
        // Remove patient-mode class for doctor layout
        document.querySelector('.game-container').classList.remove('patient-mode');
        
        // Clear chat and add initial message
        this.clearChat();
        this.addSystemMessage(gameData.message);
    }
    
    setupPatientGameUI(gameData) {
        // Use the unified game screen
        this.showScreen('game');
        
        // Update game header for patient mode
        if (this.gameTitle) this.gameTitle.textContent = 'Medical Consultation';
        if (this.roleIndicator) this.roleIndicator.textContent = 'Patient Mode';
        if (this.specialtyIndicator) this.specialtyIndicator.textContent = gameData.doctor_specialty?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'General Medicine';
        
        // Show patient info panel with user's information
        if (this.patientInfoPanel) this.patientInfoPanel.style.display = 'block';
        if (this.patientNameDisplay) this.patientNameDisplay.textContent = gameData.patient_name || 'John Doe';
        if (this.patientAgeDisplay) this.patientAgeDisplay.textContent = gameData.patient_age || '35';
        if (this.patientGenderDisplay) this.patientGenderDisplay.textContent = gameData.patient_gender || 'Male';
        if (this.chiefComplaintDisplay) this.chiefComplaintDisplay.textContent = gameData.chief_complaint || 'General consultation';
        
        // Hide diagnosis panel (not needed in patient mode)
        if (this.diagnosisPanel) this.diagnosisPanel.style.display = 'none';
        
        // Hide quick actions and guide text (not needed in patient mode)
        if (this.quickActionsDiv) this.quickActionsDiv.style.display = 'none';
        if (this.doctorGuideText) this.doctorGuideText.style.display = 'none';
        
        // Add patient-mode class for styling
        document.querySelector('.game-container').classList.add('patient-mode');
        
        // Clear chat and add initial message
        this.clearChat();
        this.addSystemMessage(gameData.message || 'Welcome to your medical consultation.');
        this.addAIMessage(gameData.initial_ai_message || "Hello! I'm Dr. Smith. How can I help you today?");
    }
    
    async sendMessage() {
        // Use unified input element for both roles since both use game screen
        const inputElement = this.messageInput;
        const message = inputElement.value.trim();
        if (!message || this.isLoading) return;
        
        try {
            // Add user message to UI
            this.addUserMessage(message);
            inputElement.value = '';
            
            // Log message send for patient mode
            if (this.currentRole === 'patient') {
                await this.logInteraction('message_sent', {
                    message: message,
                    timestamp: new Date().toISOString()
                });
            }
            
            // Disable input while processing
            this.setInputLoading(true);
            
            // Send to API with longer timeout for AI response
            const response = await this.apiCall('/api/game/message', 'POST', {
                session_id: this.currentSession,
                message: message
            }, 60000); // 60 second timeout for AI messages
            
            // Add AI response
            this.addAIMessage(response.response);
            
            // Check if user mentioned physical exam or lab tests (doctor mode only)
            if (this.currentRole === 'doctor') {
                this.checkForExamRequests(message);
            }
            
        } catch (error) {
            this.showError('Failed to send message: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    async submitDiagnosis() {
        const diagnosis = this.diagnosisInput.value.trim();
        if (!diagnosis || this.isLoading) return;
        
        try {
            this.setInputLoading(true);
            
            const response = await this.apiCall('/api/game/diagnose', 'POST', {
                session_id: this.currentSession,
                diagnosis: diagnosis
            }, 30000); // 30 second timeout
            
            this.diagnosisInput.value = '';
            this.attemptsCount.textContent = response.attempts;
            
            if (response.correct) {
                this.showDiagnosisResults(response);
            } else {
                this.addSystemMessage(response.message);
            }
            
        } catch (error) {
            this.showError('Failed to submit diagnosis: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    showDiagnosisResults(results) {
        this.resultsTitle.textContent = 'Correct Diagnosis!';
        
        const content = `
            <div class=\"results-success\">
                <div class=\"success-icon\">
                    <i class=\"fas fa-check-circle text-success\"></i>
                </div>
                <h4 class=\"success-title\">Diagnosis Correct!</h4>
                <p class=\"success-message\">${results.message}</p>
            </div>
            
            <div class=\"condition-details\">
                <h5>Condition Information:</h5>
                <div class=\"detail-grid\">
                    <div class=\"detail-item\">
                        <label>Condition:</label>
                        <span>${results.condition_info.name}</span>
                    </div>
                    <div class=\"detail-item\">
                        <label>Difficulty:</label>
                        <span>${results.condition_info.difficulty}</span>
                    </div>
                    <div class=\"detail-item\">
                        <label>Attempts:</label>
                        <span>${results.attempts}</span>
                    </div>
                </div>
                
                ${results.condition_info.treatment ? `
                    <div class=\"treatment-info\">
                        <h6>Treatment:</h6>
                        <ul>
                            ${results.condition_info.treatment.map(t => `<li>${t}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${results.condition_info.prognosis ? `
                    <div class=\"prognosis-info\">
                        <h6>Prognosis:</h6>
                        <p>${results.condition_info.prognosis}</p>
                    </div>
                ` : ''}
            </div>
        `;
        
        this.resultsContent.innerHTML = content;
        this.showModal();
    }
    
    addUserMessage(message) {
        // Use unified chat container since both roles use game screen
        const chatContainer = this.chatMessages;
        if (chatContainer) {
            const messageElement = this.createMessageElement('user', message);
            chatContainer.appendChild(messageElement);
            this.scrollToBottom();
        }
    }
    
    addAIMessage(message) {
        // Use unified chat container since both roles use game screen
        const chatContainer = this.chatMessages;
        if (chatContainer) {
            const messageElement = this.createMessageElement('ai', message);
            chatContainer.appendChild(messageElement);
            this.scrollToBottom();
        }
    }
    
    addSystemMessage(message) {
        // Use unified chat container since both roles use game screen
        const chatContainer = this.chatMessages;
        if (chatContainer) {
            const messageElement = document.createElement('div');
            messageElement.className = 'system-message';
            messageElement.style.cssText = `
                text-align: center;
                color: var(--text-secondary);
                font-style: italic;
                margin: var(--spacing-md) 0;
                padding: var(--spacing-sm);
                background: var(--background-secondary);
                border-radius: var(--radius-md);
                font-size: var(--font-size-sm);
            `;
            messageElement.textContent = message;
            chatContainer.appendChild(messageElement);
            this.scrollToBottom();
        }
    }
    
    createMessageElement(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? '<i class=\"fas fa-user\"></i>' : '<i class=\"fas fa-user-md\"></i>';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = content;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        
        return messageDiv;
    }
    
    clearChat() {
        // Use unified chat container since both roles use game screen
        const chatContainer = this.chatMessages;
        if (chatContainer) chatContainer.innerHTML = '';
    }
    
    scrollToBottom() {
        // Use unified chat container since both roles use game screen
        const chatContainer = this.chatMessages;
        if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    setInputLoading(loading) {
        // Use unified elements since both roles use game screen
        const sendBtn = this.sendMessageBtn;
        const messageInput = this.messageInput;
        
        if (sendBtn) sendBtn.disabled = loading;
        if (messageInput) messageInput.disabled = loading;
        
        if (this.submitDiagnosisBtn) {
            this.submitDiagnosisBtn.disabled = loading;
            if (this.diagnosisInput) this.diagnosisInput.disabled = loading;
        }
        
        if (sendBtn) {
            if (loading) {
                sendBtn.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i>';
            } else {
                sendBtn.innerHTML = '<i class=\"fas fa-paper-plane\"></i>';
            }
        }
    }
    
    showLoading(message = 'Loading...') {
        this.isLoading = true;
        if (this.loadingOverlay) {
            const loadingText = this.loadingOverlay.querySelector('.loading-text');
            if (loadingText) loadingText.textContent = message;
            this.loadingOverlay.classList.add('active');
        }
    }
    
    hideLoading() {
        this.isLoading = false;
        if (this.loadingOverlay) this.loadingOverlay.classList.remove('active');
    }
    
    showModal() {
        if (this.resultsModal) this.resultsModal.classList.add('active');
        // Hide ads during critical interactions
        const activeScreen = document.querySelector('.screen.active');
        if (activeScreen) activeScreen.classList.add('no-ads');
    }
    
    closeModal() {
        if (this.resultsModal) this.resultsModal.classList.remove('active');
        // Show ads again after modal closes
        const activeScreen = document.querySelector('.screen.active');
        if (activeScreen) activeScreen.classList.remove('no-ads');
    }
    
    showError(message) {
        alert('Error: ' + message);
    }
    
    showLanguageMessage() {
        alert('Sorry. Currently only English version is serviced.');
    }
    
    goToWelcome() {
        this.showScreen('welcome');
        this.currentSession = null;
        this.currentRole = null;
    }
    
    async startNewCase() {
        this.closeModal();
        if (this.currentRole === 'doctor') {
            await this.startDoctorGame();
        }
    }
    
    backToMenu() {
        this.closeModal();
        this.showScreen('welcome');
        this.currentSession = null;
    }
    
    async endGame() {
        if (confirm('Are you sure you want to finish the current session?')) {
            // Log end game action for patient mode
            if (this.currentRole === 'patient') {
                await this.logInteraction('session_end_requested', {
                    timestamp: new Date().toISOString()
                });
            }
            
            // Log the session before ending
            if (this.currentSession) {
                try {
                    await this.apiCall('/api/game/end-session', 'POST', {
                        session_id: this.currentSession
                    });
                } catch (error) {
                    console.error('Error logging session:', error);
                }
            }
            
            this.showScreen('welcome');
            this.currentSession = null;
            this.currentRole = null;
        }
    }
    
    async apiCall(endpoint, method = 'GET', data = null, timeout = 10000, maxRetries = 10) {
        let lastError = null;
        
        // Retry loop
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                const config = {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json'
                    }
                };
                
                if (data) {
                    config.body = JSON.stringify(data);
                }
                
                // Create an AbortController for timeout
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), timeout);
                config.signal = controller.signal;
                
                const response = await fetch(endpoint, config);
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    const errorMessage = errorData.detail || `HTTP ${response.status}`;
                    
                    // If it's a session not found error and we have retries left, retry
                    if ((errorMessage.includes('session not found') || errorMessage.includes('Session not found')) && attempt < maxRetries) {
                        console.log(`[RETRY ${attempt}/${maxRetries}] Session not found, retrying in ${attempt * 500}ms...`);
                        // Update UI to show retry status
                        this.updateRetryStatus(attempt, maxRetries);
                        await new Promise(resolve => setTimeout(resolve, attempt * 500)); // Exponential backoff
                        continue;
                    }
                    
                    throw new Error(errorMessage);
                }
                
                // Success - return the result
                return await response.json();
                
            } catch (error) {
                lastError = error;
                
                // Handle timeout errors
                if (error.name === 'AbortError') {
                    if (attempt < maxRetries) {
                        console.log(`[RETRY ${attempt}/${maxRetries}] Request timeout, retrying...`);
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        continue;
                    }
                    throw new Error('Request timeout after multiple attempts');
                }
                
                // For session errors, retry silently
                if ((error.message.includes('session not found') || error.message.includes('Session not found')) && attempt < maxRetries) {
                    console.log(`[RETRY ${attempt}/${maxRetries}] Session error: ${error.message}`);
                    this.updateRetryStatus(attempt, maxRetries);
                    await new Promise(resolve => setTimeout(resolve, attempt * 500));
                    continue;
                }
                
                // For other errors, check if we should retry
                if (attempt < maxRetries && !error.message.includes('400') && !error.message.includes('401')) {
                    console.log(`[RETRY ${attempt}/${maxRetries}] API error: ${error.message}`);
                    await new Promise(resolve => setTimeout(resolve, attempt * 500));
                    continue;
                }
                
                // No more retries - throw the error
                throw error;
            }
        }
        
        // All retries exhausted
        throw lastError || new Error('API call failed after ' + maxRetries + ' attempts');
    }
    
    updateRetryStatus(attempt, maxRetries) {
        // Silent retry - no visual indication of retry attempts
        // Just keep the loading animation running
        console.log(`[RETRY ${attempt}/${maxRetries}] Retrying silently...`);
    }
    
    async logInteraction(actionType, actionData) {
        // Only log if we have a current session and in patient mode
        if (!this.currentSession || this.currentRole !== 'patient') {
            return;
        }
        
        try {
            await this.apiCall('/api/game/log-interaction', 'POST', {
                session_id: this.currentSession,
                action_type: actionType,
                action_data: actionData
            });
        } catch (error) {
            // Don't interrupt user experience if logging fails
            console.error('Failed to log interaction:', error);
        }
    }
    
    async logButtonClick(buttonId, buttonText) {
        // Log button clicks for patient mode
        await this.logInteraction('button_click', {
            button_id: buttonId,
            button_text: buttonText,
            timestamp: new Date().toISOString()
        });
    }
    
    // Validation helpers
    validatePatientForm() {
        const name = this.patientNameInput.value.trim();
        const age = parseInt(this.patientAgeInput.value);
        const complaint = this.chiefComplaintInput.value.trim();
        
        if (!name) {
            this.showError('Please enter your name');
            return false;
        }
        
        if (!age || age < 1 || age > 120) {
            this.showError('Please enter a valid age (1-120)');
            return false;
        }
        
        if (!complaint) {
            this.showError('Please describe your chief complaint');
            return false;
        }
        
        return true;
    }
    
    // Context-aware button management
    resetQuickActionButtons() {
        this.pexRequested = false;
        this.labRequested = false;
        if (this.pexBtn) {
            this.pexBtn.classList.add('disabled');
            this.pexBtn.classList.remove('activated');
        }
        if (this.labTestBtn) {
            this.labTestBtn.classList.add('disabled');
            this.labTestBtn.classList.remove('activated');
        }
    }
    
    checkForExamRequests(message) {
        const lowerMessage = message.toLowerCase();
        
        // Check for physical exam keywords
        const pexKeywords = ['physical exam', 'examine', 'examination', 'check', 'listen', 'feel', 'palpate', 'auscult'];
        if (pexKeywords.some(keyword => lowerMessage.includes(keyword)) && !this.pexRequested && this.pexBtn) {
            this.pexRequested = true;
            this.pexBtn.classList.remove('disabled');
            this.pexBtn.classList.add('activated');
        }
        
        // Check for lab test keywords
        const labKeywords = ['lab', 'test', 'blood', 'urine', 'x-ray', 'scan', 'mri', 'ct', 'ecg', 'ekg'];
        if (labKeywords.some(keyword => lowerMessage.includes(keyword)) && !this.labRequested && this.labTestBtn) {
            this.labRequested = true;
            this.labTestBtn.classList.remove('disabled');
            this.labTestBtn.classList.add('activated');
        }
    }
    
    async performPhysicalExam() {
        if (!this.pexRequested || this.isLoading) return;
        
        try {
            this.setInputLoading(true);
            
            const response = await this.apiCall('/api/game/physical-exam', 'POST', {
                session_id: this.currentSession
            }, 40000); // 40 second timeout
            
            this.showPhysicalExamResults(response);
            
        } catch (error) {
            this.showError('Failed to perform physical exam: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    async performLabTests() {
        if (!this.labRequested || this.isLoading) return;
        
        try {
            this.setInputLoading(true);
            
            const response = await this.apiCall('/api/game/lab-tests', 'POST', {
                session_id: this.currentSession
            }, 40000); // 40 second timeout
            
            this.showLabTestResults(response);
            
        } catch (error) {
            this.showError('Failed to perform lab tests: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    async showAnswer() {
        if (this.isLoading) return;
        
        // Show loading message on button
        const showAnswerBtn = document.getElementById('show-answer-btn');
        const originalText = showAnswerBtn ? showAnswerBtn.innerHTML : '';
        if (showAnswerBtn) {
            showAnswerBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading answer...';
            showAnswerBtn.disabled = true;
        }
        
        try {
            this.setInputLoading(true);
            
            // First validate session exists
            if (!this.currentSession) {
                throw new Error('No active session. Please restart the game.');
            }
            
            const response = await this.apiCall('/api/game/show-answer', 'POST', {
                session_id: this.currentSession
            }, 30000); // 30 second timeout
            
            this.showAnswerResults(response);
            
        } catch (error) {
            // More specific error handling
            if (error.message.includes('timeout')) {
                this.showError('The request is taking longer than expected. Please try again.');
            } else if (error.message.includes('session not found') || error.message.includes('Session not found')) {
                this.showError('Your session has expired. Please refresh the page and start a new game.');
                console.error('Session lost:', this.currentSession);
            } else {
                this.showError('Failed to show answer: ' + error.message);
            }
        } finally {
            this.setInputLoading(false);
            // Restore button
            if (showAnswerBtn) {
                showAnswerBtn.innerHTML = originalText;
                showAnswerBtn.disabled = false;
            }
        }
    }
    
    async showMultipleChoice() {
        if (this.isLoading) return;
        
        // Show loading message on button
        const multipleChoiceBtn = document.getElementById('show-multiple-choice-btn');
        const originalText = multipleChoiceBtn ? multipleChoiceBtn.innerHTML : '';
        if (multipleChoiceBtn) {
            multipleChoiceBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading options...';
            multipleChoiceBtn.disabled = true;
        }
        
        try {
            this.setInputLoading(true);
            
            const response = await this.apiCall('/api/game/show-multiple-choice', 'POST', {
                session_id: this.currentSession
            }, 30000); // 30 second timeout
            
            if (response.error) {
                this.showError(response.message || response.error);
            } else {
                this.showMultipleChoiceModal(response);
            }
            
        } catch (error) {
            // More specific error handling
            if (error.message.includes('timeout')) {
                this.showError('The request is taking longer than expected. Please try again.');
            } else {
                this.showError('Failed to show multiple choice: ' + error.message);
            }
        } finally {
            this.setInputLoading(false);
            // Restore button
            if (multipleChoiceBtn) {
                multipleChoiceBtn.innerHTML = originalText;
                multipleChoiceBtn.disabled = false;
            }
        }
    }
    
    showPhysicalExamResults(results) {
        let content = '<h4>Physical Examination Findings</h4>';
        
        if (results.physical_findings && Array.isArray(results.physical_findings)) {
            results.physical_findings.forEach(finding => {
                content += `
                    <div class="examination-result">
                        <div class="result-label">${finding.system}</div>
                        <div class="result-value">${finding.finding}</div>
                    </div>
                `;
            });
        } else if (results.message) {
            content += `<div class="examination-result">
                <div class="result-value">${results.message}</div>
            </div>`;
        }
        
        this.pexContent.innerHTML = content;
        this.pexModal.classList.add('active');
        // Hide ads during medical examination
        const activeScreen = document.querySelector('.screen.active');
        if (activeScreen) activeScreen.classList.add('no-ads');
    }
    
    showLabTestResults(results) {
        let content = '<h4>Laboratory Test Results</h4>';
        
        if (results.lab_results && typeof results.lab_results === 'object') {
            Object.entries(results.lab_results).forEach(([test, result]) => {
                content += `
                    <div class="examination-result">
                        <div class="result-label">${test}</div>
                        <div class="result-value">${result}</div>
                    </div>
                `;
            });
        } else if (results.message) {
            content += `<div class="examination-result">
                <div class="result-value">${results.message}</div>
            </div>`;
        }
        
        this.labContent.innerHTML = content;
        this.labModal.classList.add('active');
        // Hide ads during lab results
        const activeScreen = document.querySelector('.screen.active');
        if (activeScreen) activeScreen.classList.add('no-ads');
    }
    
    showAnswerResults(results) {
        this.resultsTitle.textContent = 'Correct Answer';
        
        const content = `
            <div class="condition-details">
                <h5>Correct Diagnosis:</h5>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Condition:</label>
                        <span>${results.condition_info.name}</span>
                    </div>
                    <div class="detail-item">
                        <label>Difficulty:</label>
                        <span>${results.condition_info.difficulty}</span>
                    </div>
                </div>
                
                ${results.condition_info.description ? `
                    <div class="treatment-info">
                        <h6>Description:</h6>
                        <p>${results.condition_info.description}</p>
                    </div>
                ` : ''}
                
                ${results.condition_info.treatment ? `
                    <div class="treatment-info">
                        <h6>Treatment:</h6>
                        <ul>
                            ${results.condition_info.treatment.map(t => `<li>${t}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${results.condition_info.prognosis ? `
                    <div class="prognosis-info">
                        <h6>Prognosis:</h6>
                        <p>${results.condition_info.prognosis}</p>
                    </div>
                ` : ''}
            </div>
        `;
        
        this.resultsContent.innerHTML = content;
        this.showModal();
    }
    
    closePexModal() {
        this.pexModal.classList.remove('active');
        // Show ads again after modal closes
        const activeScreen = document.querySelector('.screen.active');
        if (activeScreen) activeScreen.classList.remove('no-ads');
    }
    
    closeLabModal() {
        this.labModal.classList.remove('active');
        // Show ads again after modal closes
        const activeScreen = document.querySelector('.screen.active');
        if (activeScreen) activeScreen.classList.remove('no-ads');
    }
    
    showMultipleChoiceModal(data) {
        this.resultsTitle.textContent = 'Multiple Choice Options';
        
        const content = `
            <div class="multiple-choice-container">
                <p class="multiple-choice-message">${data.message}</p>
                <div class="multiple-choice-options">
                    ${data.multiple_choice.map((option, index) => {
                        return `
                            <div class="multiple-choice-option clickable" data-diagnosis="${option}">
                                <span class="option-letter">${String.fromCharCode(65 + index)}.</span>
                                <span class="option-text">${option}</span>
                            </div>
                        `;
                    }).join('')}
                </div>
                <div class="multiple-choice-hint">
                    <i class="fas fa-info-circle"></i>
                    <span>Click on an option to select it as your diagnosis.</span>
                </div>
            </div>
        `;
        
        this.resultsContent.innerHTML = content;
        this.showModal();
        
        // Add click handlers to each option
        const options = this.resultsContent.querySelectorAll('.multiple-choice-option');
        options.forEach(option => {
            option.addEventListener('click', (e) => {
                const diagnosis = option.dataset.diagnosis;
                
                // Fill the diagnosis input with the selected option
                if (this.diagnosisInput) {
                    this.diagnosisInput.value = diagnosis;
                }
                
                // Close the modal
                this.closeModal();
                
                // Focus on the diagnosis input
                if (this.diagnosisInput) {
                    this.diagnosisInput.focus();
                }
            });
        });
    }
    
}

// Additional CSS for results modal (inject into head)
const additionalStyles = `
    <style>
        .results-success {
            text-align: center;
            margin-bottom: var(--spacing-xl);
        }
        
        .success-icon i {
            font-size: 3rem;
            margin-bottom: var(--spacing-md);
        }
        
        .success-title {
            font-size: var(--font-size-lg);
            font-weight: 600;
            color: var(--success-color);
            margin-bottom: var(--spacing-sm);
        }
        
        .success-message {
            color: var(--text-secondary);
        }
        
        .condition-details h5 {
            font-size: var(--font-size-base);
            font-weight: 600;
            margin-bottom: var(--spacing-md);
            color: var(--text-primary);
        }
        
        .detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: var(--spacing-md);
            margin-bottom: var(--spacing-lg);
        }
        
        .detail-grid .detail-item {
            background: var(--background-secondary);
            padding: var(--spacing-md);
            border-radius: var(--radius-md);
        }
        
        .treatment-info,
        .prognosis-info {
            margin-top: var(--spacing-lg);
        }
        
        .treatment-info h6,
        .prognosis-info h6 {
            font-size: var(--font-size-sm);
            font-weight: 600;
            margin-bottom: var(--spacing-sm);
            color: var(--text-primary);
        }
        
        .treatment-info ul {
            margin: 0;
            padding-left: var(--spacing-lg);
        }
        
        .treatment-info li {
            margin-bottom: var(--spacing-xs);
            color: var(--text-secondary);
        }
        
        .prognosis-info p {
            color: var(--text-secondary);
            margin: 0;
        }
        
        /* Multiple Choice Styles */
        .multiple-choice-container {
            padding: var(--spacing-md);
        }
        
        .multiple-choice-message {
            font-size: var(--font-size-base);
            color: var(--text-primary);
            margin-bottom: var(--spacing-lg);
        }
        
        .multiple-choice-options {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-md);
            margin-bottom: var(--spacing-lg);
        }
        
        .multiple-choice-option {
            display: flex;
            align-items: center;
            padding: var(--spacing-md);
            background: var(--background-secondary);
            border: 2px solid var(--border-color);
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
        }
        
        .multiple-choice-option.clickable {
            cursor: pointer;
        }
        
        .multiple-choice-option.clickable:hover {
            background: var(--background-hover);
            border-color: var(--primary-color);
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .option-letter {
            font-weight: 600;
            margin-right: var(--spacing-sm);
            color: var(--text-primary);
        }
        
        .option-text {
            flex: 1;
            color: var(--text-primary);
        }
        
        .multiple-choice-hint {
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            color: var(--text-secondary);
            font-size: var(--font-size-sm);
            font-style: italic;
        }
        
        .multiple-choice-hint i {
            color: #3b82f6;
        }
    </style>
`;

// Inject additional styles
document.head.insertAdjacentHTML('beforeend', additionalStyles);

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.medicalGameApp = new MedicalGameApp();
});