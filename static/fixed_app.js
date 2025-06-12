// Fixed Medical Simulation Game - Frontend JavaScript

console.log("🚀 Loading MedSim App...");

class MedicalGameApp {
    constructor() {
        console.log("📱 Initializing MedicalGameApp...");
        
        this.currentSession = null;
        this.currentRole = null;
        this.isLoading = false;
        this.currentLanguage = 'en';
        this.translations = null;
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initialize());
        } else {
            this.initialize();
        }
    }
    
    async initialize() {
        console.log("🔧 Initializing app components...");
        
        try {
            await this.loadTranslations();
            this.initializeElements();
            this.attachEventListeners();
            this.showLanguageSelection();
            console.log("✅ App initialized successfully");
        } catch (error) {
            console.error("❌ App initialization failed:", error);
            this.showError("Failed to initialize app: " + error.message);
        }
    }
    
    initializeElements() {
        console.log("🔍 Finding DOM elements...");
        
        // Screens
        this.screens = {
            welcome: this.getElement('welcome-screen'),
            setup: this.getElement('setup-screen'),
            game: this.getElement('game-screen')
        };
        
        // Navigation
        this.languageBtn = this.getElement('language-btn');
        this.currentLanguageSpan = this.getElement('current-language');
        this.backToWelcomeBtn = this.getElement('back-to-welcome');
        this.endGameBtn = this.getElement('end-game-btn');
        
        // Role selection
        this.roleCards = document.querySelectorAll('.role-card');
        console.log(`📋 Found ${this.roleCards.length} role cards`);
        
        // Setup forms
        this.doctorSetup = this.getElement('doctor-setup');
        this.patientSetup = this.getElement('patient-setup');
        this.setupTitle = this.getElement('setup-title');
        
        // Form elements
        this.difficultySelect = this.getElement('difficulty-select');
        this.specialtySelect = this.getElement('specialty-select');
        this.patientNameInput = this.getElement('patient-name');
        this.patientAgeInput = this.getElement('patient-age');
        this.patientGenderSelect = this.getElement('patient-gender');
        this.chiefComplaintInput = this.getElement('chief-complaint');
        this.doctorSpecialtySelect = this.getElement('doctor-specialty');
        
        // Game buttons
        this.startDoctorGameBtn = this.getElement('start-doctor-game');
        this.startPatientGameBtn = this.getElement('start-patient-game');
        
        // Game interface elements (may not exist initially)
        this.gameTitle = document.getElementById('game-title');
        this.roleIndicator = document.getElementById('role-indicator');
        this.difficultyIndicator = document.getElementById('difficulty-indicator');
        this.specialtyIndicator = document.getElementById('specialty-indicator');
        
        // Quick action buttons
        this.quickActions = document.getElementById('quick-actions');
        this.pexBtn = document.getElementById('pex-btn');
        this.labTestBtn = document.getElementById('lab-test-btn');
        
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
        this.showAnswerBtn = document.getElementById('show-answer-btn');
        this.attemptsCount = document.getElementById('attempts-count');
        
        // Modal
        this.resultsModal = document.getElementById('results-modal');
        this.resultsTitle = document.getElementById('results-title');
        this.resultsContent = document.getElementById('results-content');
        this.closeModalBtn = document.getElementById('close-modal');
        this.newCaseBtn = document.getElementById('new-case-btn');
        this.backToMenuBtn = document.getElementById('back-to-menu-btn');
        
        // Examination modals
        this.pexModal = document.getElementById('pex-modal');
        this.pexContent = document.getElementById('pex-content');
        this.closePexModalBtn = document.getElementById('close-pex-modal');
        this.closePexBtn = document.getElementById('close-pex-btn');
        
        this.labModal = document.getElementById('lab-modal');
        this.labContent = document.getElementById('lab-content');
        this.closeLabModalBtn = document.getElementById('close-lab-modal');
        this.closeLabBtn = document.getElementById('close-lab-btn');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loading-overlay');
        
        console.log("✅ Elements initialized");
    }
    
    getElement(id) {
        const element = document.getElementById(id);
        if (!element) {
            console.warn(`⚠️  Element not found: ${id}`);
        } else {
            console.log(`✅ Found element: ${id}`);
        }
        return element;
    }
    
    attachEventListeners() {
        console.log("🔗 Attaching event listeners...");
        
        // Navigation
        if (this.languageBtn) {
            this.languageBtn.addEventListener('click', () => {
                console.log("🌐 Language button clicked");
                this.showLanguageSelector();
            });
        }
        
        if (this.backToWelcomeBtn) {
            this.backToWelcomeBtn.addEventListener('click', () => {
                console.log("⬅️  Back to welcome clicked");
                this.showScreen('welcome');
            });
        }
        
        if (this.endGameBtn) {
            this.endGameBtn.addEventListener('click', () => this.endGame());
        }
        
        // Role selection
        this.roleCards.forEach((card, index) => {
            console.log(`🎯 Attaching listener to role card ${index}: ${card.dataset.role}`);
            card.addEventListener('click', () => {
                console.log(`🎭 Role selected: ${card.dataset.role}`);
                this.selectRole(card.dataset.role);
            });
        });
        
        // Setup buttons
        if (this.startDoctorGameBtn) {
            this.startDoctorGameBtn.addEventListener('click', () => {
                console.log("🩺 Start doctor game clicked");
                this.startDoctorGame();
            });
        }
        
        if (this.startPatientGameBtn) {
            this.startPatientGameBtn.addEventListener('click', () => {
                console.log("🤒 Start patient game clicked");
                this.startPatientGame();
            });
        }
        
        // Chat
        if (this.sendMessageBtn) {
            this.sendMessageBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (this.messageInput) {
            this.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
        
        // Diagnosis
        if (this.submitDiagnosisBtn) {
            this.submitDiagnosisBtn.addEventListener('click', () => this.submitDiagnosis());
        }
        
        if (this.showAnswerBtn) {
            this.showAnswerBtn.addEventListener('click', () => this.showAnswer());
        }
        
        // Physical examination and lab test buttons
        if (this.pexBtn) {
            this.pexBtn.addEventListener('click', () => this.performPhysicalExam());
        }
        
        if (this.labTestBtn) {
            this.labTestBtn.addEventListener('click', () => this.performLabTests());
        }
        
        // Examination modal close buttons
        if (this.closePexModalBtn) {
            this.closePexModalBtn.addEventListener('click', () => this.closePexModal());
        }
        
        if (this.closePexBtn) {
            this.closePexBtn.addEventListener('click', () => this.closePexModal());
        }
        
        if (this.closeLabModalBtn) {
            this.closeLabModalBtn.addEventListener('click', () => this.closeLabModal());
        }
        
        if (this.closeLabBtn) {
            this.closeLabBtn.addEventListener('click', () => this.closeLabModal());
        }
        
        if (this.diagnosisInput) {
            this.diagnosisInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.submitDiagnosis();
                }
            });
        }
        
        // Modal
        if (this.closeModalBtn) {
            this.closeModalBtn.addEventListener('click', () => this.closeModal());
        }
        
        if (this.newCaseBtn) {
            this.newCaseBtn.addEventListener('click', () => this.startNewCase());
        }
        
        if (this.backToMenuBtn) {
            this.backToMenuBtn.addEventListener('click', () => this.backToMenu());
        }
        
        // Modal close on background click
        if (this.resultsModal) {
            this.resultsModal.addEventListener('click', (e) => {
                if (e.target === this.resultsModal) {
                    this.closeModal();
                }
            });
        }
        
        console.log("✅ Event listeners attached");
    }
    
    showScreen(screenName) {
        console.log(`📺 Showing screen: ${screenName}`);
        
        // Hide all screens
        Object.values(this.screens).forEach(screen => {
            if (screen) {
                screen.classList.remove('active');
            }
        });
        
        // Show target screen
        if (this.screens[screenName]) {
            this.screens[screenName].classList.add('active');
            console.log(`✅ Screen ${screenName} activated`);
        } else {
            console.error(`❌ Screen not found: ${screenName}`);
        }
        
        // Reset role selection when going back to welcome
        if (screenName === 'welcome') {
            this.currentRole = null;
            this.roleCards.forEach(card => card.classList.remove('selected'));
        }
    }
    
    selectRole(role) {
        console.log(`🎭 Selecting role: ${role}`);
        this.currentRole = role;
        
        // Update UI
        this.roleCards.forEach(card => {
            card.classList.toggle('selected', card.dataset.role === role);
        });
        
        // Show setup screen after delay
        setTimeout(() => {
            this.showSetupScreen(role);
        }, 300);
    }
    
    showSetupScreen(role) {
        console.log(`⚙️  Setting up ${role} mode`);
        this.showScreen('setup');
        
        if (role === 'doctor') {
            if (this.setupTitle) this.setupTitle.textContent = this.getText('doctor_setup_title');
            if (this.doctorSetup) this.doctorSetup.style.display = 'block';
            if (this.patientSetup) this.patientSetup.style.display = 'none';
        } else {
            if (this.setupTitle) this.setupTitle.textContent = this.getText('patient_setup_title');
            if (this.doctorSetup) this.doctorSetup.style.display = 'none';
            if (this.patientSetup) this.patientSetup.style.display = 'block';
        }
        
        // Update setup form texts
        this.updateSetupFormTexts();
    }
    
    updateSetupFormTexts() {
        // Update form labels and placeholders
        const elements = {
            'difficulty-label': 'difficulty_label',
            'specialty-label': 'specialty_label',
            'patient-name-label': 'patient_name_label',
            'patient-age-label': 'patient_age_label',
            'patient-gender-label': 'patient_gender_label',
            'chief-complaint-label': 'chief_complaint_label',
            'doctor-specialty-label': 'doctor_specialty_label'
        };
        
        Object.entries(elements).forEach(([id, key]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = this.getText(key);
            }
        });
        
        // Update placeholders
        if (this.patientNameInput) {
            this.patientNameInput.placeholder = this.getText('patient_name_label');
        }
        if (this.chiefComplaintInput) {
            this.chiefComplaintInput.placeholder = this.getText('chief_complaint_placeholder');
        }
        if (this.messageInput) {
            this.messageInput.placeholder = this.getText('message_placeholder');
        }
        if (this.diagnosisInput) {
            this.diagnosisInput.placeholder = this.getText('diagnosis_placeholder');
        }
    }
    
    async startDoctorGame() {
        if (this.isLoading) return;
        
        console.log("🩺 Starting doctor game...");
        
        try {
            this.showLoading('Creating your medical case...');
            
            const difficulty = this.difficultySelect?.value || 'medium';
            const specialty = this.specialtySelect?.value || null;
            
            console.log(`📋 Doctor game settings: ${difficulty}, ${specialty}`);
            
            // Create game session
            const response = await this.apiCall('/api/game/create', 'POST', {
                role: 'doctor',
                difficulty: difficulty,
                specialty: specialty
            });
            
            console.log("✅ Doctor game created:", response);
            
            this.currentSession = response.session_id;
            
            // Setup game UI
            this.setupDoctorGameUI(response);
            this.showScreen('game');
            
        } catch (error) {
            console.error("❌ Failed to start doctor game:", error);
            this.showError('Failed to start doctor game: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    async startPatientGame() {
        if (this.isLoading) return;
        
        console.log("🤒 Starting patient game...");
        
        // Validate form first
        if (!this.validatePatientForm()) {
            return;
        }
        
        try {
            this.showLoading('Setting up your appointment...');
            
            // First create session
            const sessionResponse = await this.apiCall('/api/game/create', 'POST', {
                role: 'patient'
            });
            
            this.currentSession = sessionResponse.session_id;
            
            // Then setup patient
            const setupResponse = await this.apiCall('/api/game/setup-patient', 'POST', {
                session_id: this.currentSession,
                patient_name: this.patientNameInput.value,
                patient_age: parseInt(this.patientAgeInput.value),
                patient_gender: this.patientGenderSelect.value,
                chief_complaint: this.chiefComplaintInput.value,
                specialty: this.doctorSpecialtySelect.value
            });
            
            console.log("✅ Patient game created:", setupResponse);
            
            // Setup game UI
            this.setupPatientGameUI(setupResponse);
            this.showScreen('game');
            
        } catch (error) {
            console.error("❌ Failed to start patient game:", error);
            this.showError('Failed to start patient game: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    setupDoctorGameUI(gameData) {
        console.log("🩺 Setting up doctor game UI");
        
        // Update game header
        if (this.gameTitle) this.gameTitle.textContent = `${this.getText('patient_info')}: ${gameData.patient_name}`;
        if (this.roleIndicator) this.roleIndicator.textContent = this.getText('doctor_mode');
        if (this.difficultyIndicator) this.difficultyIndicator.textContent = gameData.difficulty.charAt(0).toUpperCase() + gameData.difficulty.slice(1);
        if (this.specialtyIndicator) this.specialtyIndicator.textContent = gameData.specialty || 'General';
        
        // Show patient info panel
        if (this.patientInfoPanel) this.patientInfoPanel.style.display = 'block';
        if (this.patientNameDisplay) this.patientNameDisplay.textContent = gameData.patient_name;
        if (this.patientAgeDisplay) this.patientAgeDisplay.textContent = gameData.patient_age;
        if (this.patientGenderDisplay) this.patientGenderDisplay.textContent = gameData.patient_gender;
        if (this.chiefComplaintDisplay) this.chiefComplaintDisplay.textContent = gameData.chief_complaint;
        
        // Show diagnosis panel and quick actions
        if (this.diagnosisPanel) this.diagnosisPanel.style.display = 'block';
        if (this.quickActions) this.quickActions.style.display = 'flex';
        
        // Clear chat and add initial message
        this.clearChat();
        this.addSystemMessage(gameData.message);
        
        // Update game UI texts
        this.updateGameUITexts();
    }
    
    updateGameUITexts() {
        // Update game interface labels
        const patientInfoTitle = document.querySelector('#patient-info-panel .panel-title');
        if (patientInfoTitle) {
            patientInfoTitle.innerHTML = `<i class="fas fa-user"></i> ${this.getText('patient_info')}`;
        }
        
        const conversationTitle = document.querySelector('.chat-title');
        if (conversationTitle) {
            conversationTitle.innerHTML = `<i class="fas fa-comments"></i> ${this.getText('conversation')}`;
        }
        
        const diagnosisTitle = document.querySelector('#diagnosis-panel .panel-title');
        if (diagnosisTitle) {
            diagnosisTitle.innerHTML = `<i class="fas fa-clipboard-check"></i> ${this.getText('submit_diagnosis')}`;
        }
        
        // Update detail labels
        const detailLabels = document.querySelectorAll('#patient-info-panel .detail-item label');
        if (detailLabels.length >= 4) {
            detailLabels[0].textContent = this.getText('name') + ':';
            detailLabels[1].textContent = this.getText('age') + ':';
            detailLabels[2].textContent = this.getText('gender') + ':';
            detailLabels[3].textContent = this.getText('chief_complaint') + ':';
        }
        
        // Update buttons
        const submitBtn = document.querySelector('#submit-diagnosis-btn');
        if (submitBtn) {
            submitBtn.innerHTML = `<i class="fas fa-check"></i> ${this.getText('')}`;
        }
        
        const endGameBtn = document.querySelector('#end-game-btn');
        if (endGameBtn) {
            endGameBtn.innerHTML = `<i class="fas fa-stop"></i> ${this.getText('end_game')}`;
        }
    }
    
    setupPatientGameUI(gameData) {
        console.log("🤒 Setting up patient game UI");
        
        // Update game header
        if (this.gameTitle) this.gameTitle.textContent = this.getText('consultation_with');
        if (this.roleIndicator) this.roleIndicator.textContent = this.getText('patient_mode');
        if (this.difficultyIndicator) this.difficultyIndicator.textContent = '-';
        if (this.specialtyIndicator) this.specialtyIndicator.textContent = gameData.doctor_specialty?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'General';
        
        // Hide patient info, diagnosis panels, and quick actions for patient mode
        if (this.patientInfoPanel) this.patientInfoPanel.style.display = 'none';
        if (this.diagnosisPanel) this.diagnosisPanel.style.display = 'none';
        if (this.quickActions) this.quickActions.style.display = 'none';
        
        // Clear chat and add initial message
        this.clearChat();
        this.addSystemMessage(gameData.message);
        this.addAIMessage(this.getText('doctor_greeting'));
        
        // Update game UI texts
        this.updateGameUITexts();
    }
    
    async sendMessage() {
        const message = this.messageInput?.value?.trim();
        if (!message || this.isLoading) return;
        
        console.log(`💬 Sending message: ${message}`);
        
        try {
            // Add user message to UI
            this.addUserMessage(message);
            this.messageInput.value = '';
            
            // Disable input while processing
            this.setInputLoading(true);
            
            // Send to API
            const response = await this.apiCall('/api/game/message', 'POST', {
                session_id: this.currentSession,
                message: message
            });
            
            console.log("✅ AI response received");
            
            // Add AI response
            this.addAIMessage(response.response);
            
        } catch (error) {
            console.error("❌ Failed to send message:", error);
            this.showError('Failed to send message: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    async submitDiagnosis() {
        const diagnosis = this.diagnosisInput?.value?.trim();
        if (!diagnosis || this.isLoading) return;
        
        console.log(`🔍 Submitting diagnosis: ${diagnosis}`);
        
        try {
            this.setInputLoading(true);
            
            const response = await this.apiCall('/api/game/diagnose', 'POST', {
                session_id: this.currentSession,
                diagnosis: diagnosis
            });
            
            this.diagnosisInput.value = '';
            if (this.attemptsCount) this.attemptsCount.textContent = response.attempts;
            
            if (response.correct) {
                console.log("🎉 Correct diagnosis!");
                this.showDiagnosisResults(response);
            } else {
                console.log("❌ Incorrect diagnosis");
                this.addSystemMessage(response.message);
            }
            
        } catch (error) {
            console.error("❌ Failed to submit diagnosis:", error);
            this.showError('Failed to submit diagnosis: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    async showAnswer() {
        if (!this.currentSession || this.isLoading) return;
        
        console.log("💡 Showing answer...");
        
        try {
            this.setInputLoading(true);
            
            const response = await this.apiCall('/api/game/show-answer', 'POST', {
                session_id: this.currentSession
            });
            
            console.log("✅ Answer retrieved:", response);
            this.showDiagnosisResults(response);
            
        } catch (error) {
            console.error("❌ Failed to get answer:", error);
            this.showError('Failed to get answer: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    async performPhysicalExam() {
        if (!this.currentSession || this.isLoading) return;
        
        console.log("🩺 Performing physical examination...");
        
        try {
            this.setInputLoading(true);
            
            // Send request for physical examination
            const response = await this.apiCall('/api/game/physical-exam', 'POST', {
                session_id: this.currentSession
            });
            
            console.log("✅ Physical exam results received:", response);
            this.showPexResults(response);
            
        } catch (error) {
            console.error("❌ Failed to perform physical exam:", error);
            this.showError('Failed to perform physical examination: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    async performLabTests() {
        if (!this.currentSession || this.isLoading) return;
        
        console.log("🧪 Performing laboratory tests...");
        
        try {
            this.setInputLoading(true);
            
            // Send request for lab tests
            const response = await this.apiCall('/api/game/lab-tests', 'POST', {
                session_id: this.currentSession
            });
            
            console.log("✅ Lab test results received:", response);
            this.showLabResults(response);
            
        } catch (error) {
            console.error("❌ Failed to perform lab tests:", error);
            this.showError('Failed to perform laboratory tests: ' + error.message);
        } finally {
            this.setInputLoading(false);
        }
    }
    
    showPexResults(results) {
        if (!this.pexModal || !this.pexContent) {
            console.error("❌ PEx modal elements not found");
            alert(`Physical Examination Results:\n${JSON.stringify(results, null, 2)}`);
            return;
        }
        
        let content = `<h4>Physical Examination Findings</h4>`;
        
        if (results.physical_findings) {
            results.physical_findings.forEach(finding => {
                content += `
                    <div class="examination-result">
                        <div class="result-label">${finding.system || 'General'}</div>
                        <div class="result-value">${finding.finding}</div>
                    </div>
                `;
            });
        } else {
            content += `
                <div class="examination-result">
                    <div class="result-label">Physical Examination</div>
                    <div class="result-value">${results.message || 'Physical examination completed'}</div>
                </div>
            `;
        }
        
        this.pexContent.innerHTML = content;
        this.showPexModal();
    }
    
    showLabResults(results) {
        if (!this.labModal || !this.labContent) {
            console.error("❌ Lab modal elements not found");
            alert(`Laboratory Results:\n${JSON.stringify(results, null, 2)}`);
            return;
        }
        
        let content = `<h4>Laboratory Test Results</h4>`;
        
        if (results.lab_results) {
            Object.entries(results.lab_results).forEach(([test, value]) => {
                const isAbnormal = results.abnormal_values && results.abnormal_values.includes(test);
                content += `
                    <div class="examination-result">
                        <div class="result-label">${test}</div>
                        <div class="result-value ${isAbnormal ? 'result-abnormal' : 'result-normal'}">${value}</div>
                    </div>
                `;
            });
        } else {
            content += `
                <div class="examination-result">
                    <div class="result-label">Laboratory Tests</div>
                    <div class="result-value">${results.message || 'Laboratory tests completed'}</div>
                </div>
            `;
        }
        
        this.labContent.innerHTML = content;
        this.showLabModal();
    }
    
    showPexModal() {
        if (this.pexModal) {
            this.pexModal.classList.add('active');
        }
    }
    
    closePexModal() {
        if (this.pexModal) {
            this.pexModal.classList.remove('active');
        }
    }
    
    showLabModal() {
        if (this.labModal) {
            this.labModal.classList.add('active');
        }
    }
    
    closeLabModal() {
        if (this.labModal) {
            this.labModal.classList.remove('active');
        }
    }
    
    // Utility methods
    addUserMessage(message) {
        if (!this.chatMessages) return;
        
        const messageElement = this.createMessageElement('user', message);
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    addAIMessage(message) {
        if (!this.chatMessages) return;
        
        const messageElement = this.createMessageElement('ai', message);
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    addSystemMessage(message) {
        if (!this.chatMessages) return;
        
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
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    createMessageElement(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-user-md"></i>';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = content;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        
        return messageDiv;
    }
    
    clearChat() {
        if (this.chatMessages) {
            this.chatMessages.innerHTML = '';
        }
    }
    
    scrollToBottom() {
        if (this.chatMessages) {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }
    
    setInputLoading(loading) {
        if (this.sendMessageBtn) {
            this.sendMessageBtn.disabled = loading;
            this.sendMessageBtn.innerHTML = loading ? 
                '<i class="fas fa-spinner fa-spin"></i>' : 
                '<i class="fas fa-paper-plane"></i>';
        }
        
        if (this.messageInput) {
            this.messageInput.disabled = loading;
        }
        
        if (this.submitDiagnosisBtn) {
            this.submitDiagnosisBtn.disabled = loading;
        }
        
        if (this.diagnosisInput) {
            this.diagnosisInput.disabled = loading;
        }
    }
    
    showLoading(message = 'Loading...') {
        console.log(`⏳ Loading: ${message}`);
        this.isLoading = true;
        
        if (this.loadingOverlay) {
            const loadingText = this.loadingOverlay.querySelector('.loading-text');
            if (loadingText) loadingText.textContent = message;
            this.loadingOverlay.classList.add('active');
        }
    }
    
    hideLoading() {
        console.log("✅ Loading complete");
        this.isLoading = false;
        
        if (this.loadingOverlay) {
            this.loadingOverlay.classList.remove('active');
        }
    }
    
    showError(message) {
        console.error(`❌ Error: ${message}`);
        alert('Error: ' + message);
    }
    
    validatePatientForm() {
        const name = this.patientNameInput?.value?.trim();
        const age = parseInt(this.patientAgeInput?.value);
        const complaint = this.chiefComplaintInput?.value?.trim();
        
        if (!name) {
            this.showError(this.getText('error_name_required'));
            return false;
        }
        
        if (!age || age < 1 || age > 120) {
            this.showError(this.getText('error_age_invalid'));
            return false;
        }
        
        if (!complaint) {
            this.showError(this.getText('error_complaint_required'));
            return false;
        }
        
        return true;
    }
    
    async apiCall(endpoint, method = 'GET', data = null) {
        console.log(`🌐 API call: ${method} ${endpoint}`);
        
        const config = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, config);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }
        
        const result = await response.json();
        console.log(`✅ API response:`, result);
        return result;
    }
    
    // Diagnosis results display
    showDiagnosisResults(results) {
        console.log("🎊 Showing diagnosis results:", results);
        
        if (!this.resultsModal || !this.resultsTitle || !this.resultsContent) {
            console.error("❌ Results modal elements not found");
            alert(`Correct! You diagnosed: ${results.condition_info.name}`);
            return;
        }
        
        this.resultsTitle.textContent = this.getText('correct_diagnosis');
        
        const content = `
            <div class="results-success">
                <div class="success-icon">
                    <i class="fas fa-check-circle text-success"></i>
                </div>
                <h4 class="success-title">${this.getText('diagnosis_correct')}</h4>
                <p class="success-message">${results.message}</p>
            </div>
            
            <div class="condition-details">
                <h5>${this.getText('condition_info')}:</h5>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>${this.getText('condition')}:</label>
                        <span>${results.condition_info.name}</span>
                    </div>
                    <div class="detail-item">
                        <label>${this.getText('difficulty')}:</label>
                        <span>${results.condition_info.difficulty}</span>
                    </div>
                    <div class="detail-item">
                        <label>${this.getText('attempts')}:</label>
                        <span>${results.attempts}</span>
                    </div>
                </div>
                
                ${results.condition_info.treatment ? `
                    <div class="treatment-info">
                        <h6>${this.getText('treatment')}:</h6>
                        <ul>
                            ${results.condition_info.treatment.map(t => `<li>${t}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${results.condition_info.prognosis ? `
                    <div class="prognosis-info">
                        <h6>${this.getText('prognosis')}:</h6>
                        <p>${results.condition_info.prognosis}</p>
                    </div>
                ` : ''}
            </div>
        `;
        
        this.resultsContent.innerHTML = content;
        this.showModal();
    }
    
    showModal() {
        if (this.resultsModal) {
            this.resultsModal.classList.add('active');
        }
    }
    
    closeModal() {
        if (this.resultsModal) {
            this.resultsModal.classList.remove('active');
        }
    }
    
    startNewCase() {
        this.closeModal();
        
        // Clear current session to force new case generation
        const oldSession = this.currentSession;
        this.currentSession = null;
        
        // Clear any cached data
        this.clearChat();
        if (this.diagnosisInput) this.diagnosisInput.value = '';
        if (this.attemptsCount) this.attemptsCount.textContent = '0';
        
        console.log(`🔄 Starting completely new case (was session: ${oldSession})`);
        
        if (this.currentRole === 'doctor') {
            console.log("🩺 Generating new doctor case with fresh medical condition...");
            this.startDoctorGame();
        } else if (this.currentRole === 'patient') {
            console.log("🤒 Starting new patient case...");
            this.startPatientGame();
        }
    }
    
    backToMenu() {
        this.closeModal();
        this.showScreen('welcome');
        this.currentSession = null;
    }
    
    endGame() {
        if (confirm('Are you sure you want to end the current game?')) {
            this.showScreen('welcome');
            this.currentSession = null;
        }
    }
    
    // Language management methods
    async loadTranslations() {
        try {
            console.log('🌐 Loading translations...');
            const response = await fetch('/static/languages.json');
            if (!response.ok) {
                throw new Error(`Failed to load translations: ${response.status}`);
            }
            this.translations = await response.json();
            console.log('✅ Translations loaded successfully');
        } catch (error) {
            console.error('❌ Failed to load translations:', error);
            console.log('🔄 Using fallback translations');
            // Comprehensive fallback to English defaults
            this.translations = {
                en: {
                    app_title: "MedSim - Medical Education Game",
                    nav_new_game: "New Game",
                    hero_title: "Medical Simulation Training",
                    hero_subtitle: "Practice medical diagnosis and patient care with AI-powered simulations",
                    choose_role: "Choose Your Role",
                    choose_language: "Choose Language",
                    doctor_role_title: "Doctor",
                    doctor_role_description: "Diagnose patients, order tests, and provide treatment plans",
                    doctor_feature_1: "Diagnostic challenges",
                    doctor_feature_2: "AI patients with hidden conditions",
                    doctor_feature_3: "Clinical reasoning practice",
                    patient_role_title: "Patient",
                    patient_role_description: "Experience healthcare from the patient perspective",
                    patient_feature_1: "Interact with AI doctors",
                    patient_feature_2: "Learn communication skills",
                    patient_feature_3: "Understand patient experience",
                    back: "Back",
                    doctor_setup_title: "Doctor Mode Setup",
                    patient_setup_title: "Patient Mode Setup",
                    difficulty_label: "Difficulty Level",
                    specialty_label: "Medical Specialty (Optional)",
                    patient_name_label: "Your Name",
                    patient_age_label: "Age",
                    patient_gender_label: "Gender",
                    chief_complaint_label: "Chief Complaint",
                    chief_complaint_placeholder: "Describe your main symptoms",
                    doctor_specialty_label: "Doctor Specialty",
                    start_doctor_game: "Start Doctor Game",
                    start_patient_game: "Start Patient Game",
                    patient_info: "Patient Information",
                    name: "Name",
                    age: "Age",
                    gender: "Gender",
                    chief_complaint: "Chief Complaint",
                    conversation: "Conversation",
                    message_placeholder: "Type your message...",
                    submit_diagnosis: "Submit Diagnosis",
                    diagnosis_placeholder: "Enter your diagnosis...",
                    submit: "Submit",
                    attempts: "Attempts",
                    correct_diagnosis: "Correct Diagnosis!",
                    incorrect_diagnosis: "Incorrect Diagnosis",
                    diagnosis_correct: "Diagnosis Correct!",
                    condition_info: "Condition Information",
                    condition: "Condition",
                    difficulty: "Difficulty",
                    treatment: "Treatment",
                    prognosis: "Prognosis",
                    new_case: "New Case",
                    main_menu: "Main Menu",
                    end_game: "End Game",
                    doctor_mode: "Doctor Mode",
                    patient_mode: "Patient Mode",
                    consultation_with: "Consultation with Dr. Smith",
                    doctor_greeting: "Hello! I'm Dr. Smith. I understand you're here because you're not feeling well. Can you tell me what's been bothering you?",
                    error_name_required: "Please enter your name",
                    error_age_invalid: "Please enter a valid age (1-120)",
                    error_complaint_required: "Please describe your chief complaint"
                }
            };
        }
    }
    
    getText(key) {
        if (!this.translations || !this.translations[this.currentLanguage]) {
            return key; // Fallback to key if translations not loaded
        }
        return this.translations[this.currentLanguage][key] || key;
    }
    
    setLanguage(lang) {
        console.log(`🌐 Setting language to: ${lang}`);
        this.currentLanguage = lang;
        this.updateUITexts();
        this.updateLanguageDisplay();
        localStorage.setItem('medSim_language', lang);
    }
    
    updateLanguageDisplay() {
        if (this.currentLanguageSpan) {
            const langMap = {
                'en': 'EN',
                'ko': '한',
                'ja': '日',
                'es': 'ES'
            };
            this.currentLanguageSpan.textContent = langMap[this.currentLanguage] || 'EN';
        }
    }
    
    showLanguageSelector() {
        // Force show language selection overlay
        this.createLanguageSelectionOverlay();
    }
    
    showLanguageSelection() {
        // Check if user has a saved language preference
        const savedLang = localStorage.getItem('medSim_language');
        if (savedLang && this.translations[savedLang]) {
            console.log(`🌐 Using saved language: ${savedLang}`);
            this.currentLanguage = savedLang;
            this.updateUITexts();
            this.showScreen('welcome');
            return;
        }
        
        // Skip language selection in development mode or if user prefers
        const skipLanguageSelection = localStorage.getItem('medSim_skipLanguageSelection') === 'true';
        if (skipLanguageSelection) {
            console.log('🌐 Skipping language selection (user preference)');
            this.currentLanguage = 'en';
            this.updateUITexts();
            this.showScreen('welcome');
            return;
        }
        
        // If translations failed to load or only English available, skip
        if (!this.translations || Object.keys(this.translations).length <= 1) {
            console.log('🌐 Skipping language selection (only English available)');
            this.currentLanguage = 'en';
            this.updateUITexts();
            this.showScreen('welcome');
            return;
        }
        
        // Auto-skip if this is a development environment
        if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
            console.log('🌐 Skipping language selection (development mode)');
            this.currentLanguage = 'en';
            this.updateUITexts();
            this.showScreen('welcome');
            return;
        }
        
        // Create language selection overlay
        this.createLanguageSelectionOverlay();
    }
    
    createLanguageSelectionOverlay() {
        // Remove existing overlay if present
        const existing = document.getElementById('language-selection-overlay');
        if (existing) {
            existing.remove();
        }
        
        const overlay = document.createElement('div');
        overlay.id = 'language-selection-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(5px);
        `;
        
        const modal = document.createElement('div');
        modal.style.cssText = `
            background: white;
            border-radius: 12px;
            padding: 2rem;
            max-width: 400px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        `;
        
        const languages = [
            { code: 'en', name: 'English', flag: '🇺🇸' },
            { code: 'ko', name: '한국어', flag: '🇰🇷' },
            { code: 'ja', name: '日本語', flag: '🇯🇵' },
            { code: 'es', name: 'Español', flag: '🇪🇸' }
        ];
        
        modal.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h2 style="margin: 0; color: #333;">Choose Language / 언어 선택</h2>
                <button 
                    onclick="window.gameApp.closeLanguageSelector()"
                    style="
                        background: none;
                        border: none;
                        font-size: 1.5rem;
                        color: #666;
                        cursor: pointer;
                        padding: 0.25rem;
                        border-radius: 50%;
                        width: 32px;
                        height: 32px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    "
                    onmouseover="this.style.background='#f3f4f6';"
                    onmouseout="this.style.background='none';"
                    title="Close"
                >
                    ×
                </button>
            </div>
            <div style="display: grid; gap: 1rem;">
                ${languages.map(lang => `
                    <button 
                        onclick="window.gameApp.selectLanguage('${lang.code}')"
                        style="
                            padding: 1rem;
                            border: 2px solid #e5e7eb;
                            border-radius: 12px;
                            background: white;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            font-size: 1.1rem;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            gap: 0.5rem;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        "
                        onmouseover="this.style.borderColor='#e4643d'; this.style.background='#fef2f2'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)';"
                        onmouseout="this.style.borderColor='#e5e7eb'; this.style.background='white'; this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';"
                    >
                        <span style="font-size: 1.5rem;">${lang.flag}</span>
                        <span>${lang.name}</span>
                    </button>
                `).join('')}
            </div>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e5e7eb; text-align: center;">
                <button 
                    onclick="window.gameApp.skipLanguageSelection()"
                    style="
                        padding: 0.75rem 1.5rem;
                        border: 1px solid #d1d5db;
                        border-radius: 8px;
                        background: #f9fafb;
                        cursor: pointer;
                        font-size: 0.875rem;
                        color: #6b7280;
                        transition: all 0.2s ease;
                    "
                    onmouseover="this.style.background='#e5e7eb';"
                    onmouseout="this.style.background='#f9fafb';"
                >
                    Skip (Use English)
                </button>
            </div>
        `;
        
        overlay.appendChild(modal);
        document.body.appendChild(overlay);
        
        console.log('🌐 Language selection overlay created');
    }
    
    skipLanguageSelection() {
        console.log('🌐 User chose to skip language selection');
        localStorage.setItem('medSim_skipLanguageSelection', 'true');
        this.selectLanguage('en');
    }
    
    closeLanguageSelector() {
        console.log('🌐 User closed language selector');
        const overlay = document.getElementById('language-selection-overlay');
        if (overlay) {
            overlay.remove();
        }
        // If no language was selected, default to English
        if (!this.currentLanguage || this.currentLanguage === 'en') {
            this.currentLanguage = 'en';
            this.updateUITexts();
            this.updateLanguageDisplay();
            this.showScreen('welcome');
        }
    }
    
    selectLanguage(lang) {
        console.log(`🌐 Language selected: ${lang}`);
        this.setLanguage(lang);
        
        // Remove language selection overlay
        const overlay = document.getElementById('language-selection-overlay');
        if (overlay) {
            overlay.remove();
        }
        
        // Show welcome screen
        this.showScreen('welcome');
    }
    
    updateUITexts() {
        // Update page title
        document.title = this.getText('app_title');
        
        // Update static text elements that exist in the HTML
        const textMappings = {
            'nav-new-game-text': 'nav_new_game',
            'hero-title': 'hero_title',
            'hero-subtitle': 'hero_subtitle',
            'role-selection-title': 'choose_role'
        };
        
        Object.entries(textMappings).forEach(([id, key]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = this.getText(key);
            }
        });
        
        // Update role cards
        const doctorCard = document.querySelector('[data-role="doctor"]');
        if (doctorCard) {
            const title = doctorCard.querySelector('.role-title');
            const description = doctorCard.querySelector('.role-description');
            const features = doctorCard.querySelectorAll('.role-features li');
            
            if (title) title.textContent = this.getText('doctor_role_title');
            if (description) description.textContent = this.getText('doctor_role_description');
            if (features[0]) features[0].innerHTML = `<i class="fas fa-check"></i> ${this.getText('doctor_feature_1')}`;
            if (features[1]) features[1].innerHTML = `<i class="fas fa-check"></i> ${this.getText('doctor_feature_2')}`;
            if (features[2]) features[2].innerHTML = `<i class="fas fa-check"></i> ${this.getText('doctor_feature_3')}`;
        }
        
        const patientCard = document.querySelector('[data-role="patient"]');
        if (patientCard) {
            const title = patientCard.querySelector('.role-title');
            const description = patientCard.querySelector('.role-description');
            const features = patientCard.querySelectorAll('.role-features li');
            
            if (title) title.textContent = this.getText('patient_role_title');
            if (description) description.textContent = this.getText('patient_role_description');
            if (features[0]) features[0].innerHTML = `<i class="fas fa-check"></i> ${this.getText('patient_feature_1')}`;
            if (features[1]) features[1].innerHTML = `<i class="fas fa-check"></i> ${this.getText('patient_feature_2')}`;
            if (features[2]) features[2].innerHTML = `<i class="fas fa-check"></i> ${this.getText('patient_feature_3')}`;
        }
        
        console.log(`✅ UI texts updated for language: ${this.currentLanguage}`);
    }
}

// Initialize the app when DOM is loaded
console.log("🔄 Setting up app initialization...");

let gameApp = null;

// Try multiple initialization strategies
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log("📱 DOM loaded, creating app...");
        gameApp = new MedicalGameApp();
    });
} else {
    console.log("📱 DOM already loaded, creating app immediately...");
    gameApp = new MedicalGameApp();
}

// Global access for debugging
window.gameApp = gameApp;

console.log("✅ App setup complete");