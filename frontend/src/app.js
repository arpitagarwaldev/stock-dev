class StockTradingApp {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.socket = null;
        this.currentUser = null;
        this.selectedStock = null;
        this.searchTimeout = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
        this.initializeWebSocket();
    }

    setupEventListeners() {
        // Auth modal events
        document.getElementById('loginTab').addEventListener('click', () => this.switchAuthTab('login'));
        document.getElementById('registerTab').addEventListener('click', () => this.switchAuthTab('register'));
        document.getElementById('authForm').addEventListener('submit', (e) => this.handleAuth(e));

        // Navigation events
        document.getElementById('portfolioBtn').addEventListener('click', () => this.showSection('portfolio'));
        document.getElementById('tradingBtn').addEventListener('click', () => this.showSection('trading'));
        document.getElementById('watchlistBtn').addEventListener('click', () => this.showSection('watchlist'));
        document.getElementById('historyBtn').addEventListener('click', () => this.showSection('history'));
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());

        // Trading events
        document.getElementById('stockSearch').addEventListener('input', (e) => this.handleStockSearch(e));
        document.getElementById('shareQuantity').addEventListener('input', () => this.updateTradeEstimate());
        document.getElementById('buyBtn').addEventListener('click', () => this.executeTrade('buy'));
        document.getElementById('sellBtn').addEventListener('click', () => this.executeTrade('sell'));
        document.getElementById('addWatchlistBtn').addEventListener('click', () => this.addToWatchlist());

        // Close search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-box')) {
                document.getElementById('searchResults').innerHTML = '';
            }
        });
    }

    initializeWebSocket() {
        this.socket = io('http://localhost:5000');
        
        this.socket.on('connect', () => {
            console.log('Connected to WebSocket');
        });

        this.socket.on('price_update', (data) => {
            this.handlePriceUpdate(data);
        });

        this.socket.on('error', (error) => {
            console.error('WebSocket error:', error);
        });
    }

    async checkAuthStatus() {
        try {
            const response = await fetch(`${this.apiBase}/auth/me`, {
                credentials: 'include'
            });
            
            if (response.ok) {
                const data = await response.json();
                this.currentUser = data.user;
                this.hideAuthModal();
                this.loadDashboard();
            } else {
                this.showAuthModal();
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            this.showAuthModal();
        }
    }

    switchAuthTab(tab) {
        const loginTab = document.getElementById('loginTab');
        const registerTab = document.getElementById('registerTab');
        const emailGroup = document.getElementById('emailGroup');
        const authSubmit = document.getElementById('authSubmit');

        if (tab === 'login') {
            loginTab.classList.add('active');
            registerTab.classList.remove('active');
            emailGroup.style.display = 'none';
            authSubmit.textContent = 'Login';
        } else {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            emailGroup.style.display = 'block';
            authSubmit.textContent = 'Register';
        }
    }

    async handleAuth(e) {
        e.preventDefault();
        
        const isLogin = document.getElementById('loginTab').classList.contains('active');
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();

        if (!username) {
            this.showMessage('Username is required', 'error');
            return;
        }

        const endpoint = isLogin ? '/auth/login' : '/auth/register';
        const payload = { username };
        
        if (!isLogin && email) {
            payload.email = email;
        }

        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = data.user;
                this.hideAuthModal();
                this.loadDashboard();
                this.showToast(data.message, 'success');
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            console.error('Auth error:', error);
            this.showMessage('Authentication failed. Please try again.', 'error');
        }
    }

    async logout() {
        try {
            await fetch(`${this.apiBase}/auth/logout`, {
                method: 'POST',
                credentials: 'include'
            });
            
            this.currentUser = null;
            this.showAuthModal();
            this.socket.disconnect();
        } catch (error) {
            console.error('Logout error:', error);
        }
    }

    showAuthModal() {
        document.getElementById('authModal').style.display = 'flex';
    }

    hideAuthModal() {
        document.getElementById('authModal').style.display = 'none';
    }

    showMessage(message, type = 'info') {
        const messageEl = document.getElementById('authMessage');
        messageEl.textContent = message;
        messageEl.className = `message ${type}`;
    }

    showSection(section) {
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById(`${section}Btn`).classList.add('active');

        // Update sections
        document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
        document.getElementById(`${section}Section`).classList.add('active');

        // Load section data
        switch (section) {
            case 'portfolio':
                this.loadPortfolio();
                break;
            case 'trading':
                this.loadAIRecommendations();
                break;
            case 'watchlist':
                this.loadWatchlist();
                break;
            case 'history':
                this.loadTransactionHistory();
                break;
        }
    }

    async loadDashboard() {
        await this.loadPortfolio();
        this.showSection('portfolio');
    }

    async loadPortfolio() {
        try {
            const response = await fetch(`${this.apiBase}/trading/portfolio`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.updatePortfolioDisplay(data.portfolio);
            } else {
                this.showToast('Failed to load portfolio', 'error');
            }
        } catch (error) {
            console.error('Portfolio load error:', error);
            this.showToast('Failed to load portfolio', 'error');
        }
    }

    updatePortfolioDisplay(portfolio) {
        // Update balance display
        document.getElementById('userBalance').textContent = this.formatCurrency(portfolio.balance);
        document.getElementById('totalValue').textContent = this.formatCurrency(portfolio.total_value);
        document.getElementById('cashBalance').textContent = this.formatCurrency(portfolio.balance);
        document.getElementById('portfolioValue').textContent = this.formatCurrency(portfolio.portfolio_value);
        
        const gainLossEl = document.getElementById('totalGainLoss');
        gainLossEl.textContent = this.formatCurrency(portfolio.total_gain_loss);
        gainLossEl.className = `value ${portfolio.total_gain_loss >= 0 ? 'text-success' : 'text-danger'}`;

        // Update holdings table
        const tbody = document.getElementById('holdingsBody');
        
        if (portfolio.portfolio.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="no-data">No holdings yet. Start trading to build your portfolio!</td></tr>';
        } else {
            tbody.innerHTML = portfolio.portfolio.map(holding => `
                <tr>
                    <td><strong>${holding.symbol}</strong></td>
                    <td>${holding.shares}</td>
                    <td>${this.formatCurrency(holding.avg_price)}</td>
                    <td>${this.formatCurrency(holding.current_price)}</td>
                    <td>${this.formatCurrency(holding.market_value)}</td>
                    <td class="${holding.gain_loss >= 0 ? 'text-success' : 'text-danger'}">
                        ${this.formatCurrency(holding.gain_loss)} (${holding.gain_loss_percent.toFixed(2)}%)
                    </td>
                    <td>
                        <button onclick="app.selectStockForTrading('${holding.symbol}')" class="btn btn-sm">Trade</button>
                    </td>
                </tr>
            `).join('');
        }

        // Subscribe to price updates for holdings
        portfolio.portfolio.forEach(holding => {
            this.socket.emit('subscribe_stock', { symbol: holding.symbol });
        });
    }

    async handleStockSearch(e) {
        const query = e.target.value.trim();
        
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }

        if (query.length < 1) {
            document.getElementById('searchResults').innerHTML = '';
            return;
        }

        this.searchTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`${this.apiBase}/stocks/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();

                if (data.success) {
                    this.displaySearchResults(data.results);
                }
            } catch (error) {
                console.error('Search error:', error);
            }
        }, 300);
    }

    displaySearchResults(results) {
        const container = document.getElementById('searchResults');
        
        if (results.length === 0) {
            container.innerHTML = '<div class="search-result">No stocks found</div>';
            return;
        }

        container.innerHTML = results.map(stock => `
            <div class="search-result" onclick="app.selectStock('${stock.symbol}')">
                <div class="result-symbol">${stock.symbol}</div>
                <div class="result-name">${stock.name}</div>
                <div class="result-price">${this.formatCurrency(stock.price)}</div>
            </div>
        `).join('');
    }

    async selectStock(symbol) {
        try {
            const response = await fetch(`${this.apiBase}/stocks/info/${symbol}`);
            const data = await response.json();

            if (data.success) {
                this.selectedStock = data.stock;
                this.displayStockInfo(data.stock);
                document.getElementById('searchResults').innerHTML = '';
                
                // Subscribe to price updates
                this.socket.emit('subscribe_stock', { symbol: symbol });
            }
        } catch (error) {
            console.error('Stock info error:', error);
            this.showToast('Failed to load stock information', 'error');
        }
    }

    selectStockForTrading(symbol) {
        this.showSection('trading');
        document.getElementById('stockSearch').value = symbol;
        this.selectStock(symbol);
    }

    displayStockInfo(stock) {
        document.getElementById('stockName').textContent = `${stock.symbol} - ${stock.name}`;
        document.getElementById('stockPrice').textContent = this.formatCurrency(stock.price);
        
        const changeEl = document.getElementById('stockChange');
        const changeText = `${stock.change >= 0 ? '+' : ''}${this.formatCurrency(stock.change)} (${stock.changePercent.toFixed(2)}%)`;
        changeEl.textContent = changeText;
        changeEl.className = `change ${stock.change >= 0 ? 'positive' : 'negative'}`;

        document.getElementById('stockInfo').style.display = 'block';
        this.updateTradeEstimate();
    }

    updateTradeEstimate() {
        if (!this.selectedStock) return;

        const shares = parseInt(document.getElementById('shareQuantity').value) || 0;
        const estimate = shares * this.selectedStock.price;
        document.getElementById('tradeEstimate').textContent = `Estimated cost: ${this.formatCurrency(estimate)}`;
    }

    async executeTrade(type) {
        if (!this.selectedStock) {
            this.showToast('Please select a stock first', 'warning');
            return;
        }

        const shares = parseInt(document.getElementById('shareQuantity').value);
        if (!shares || shares <= 0) {
            this.showToast('Please enter a valid number of shares', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/trading/${type}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    symbol: this.selectedStock.symbol,
                    shares: shares
                })
            });

            const data = await response.json();

            if (data.success) {
                this.showToast(data.message, 'success');
                this.loadPortfolio(); // Refresh portfolio
                document.getElementById('shareQuantity').value = '1';
                this.updateTradeEstimate();
            } else {
                this.showToast(data.message, 'error');
            }
        } catch (error) {
            console.error('Trade error:', error);
            this.showToast('Trade failed. Please try again.', 'error');
        }
    }

    async addToWatchlist() {
        if (!this.selectedStock) {
            this.showToast('Please select a stock first', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/trading/watchlist`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    symbol: this.selectedStock.symbol
                })
            });

            const data = await response.json();
            this.showToast(data.message, data.success ? 'success' : 'warning');
        } catch (error) {
            console.error('Watchlist error:', error);
            this.showToast('Failed to add to watchlist', 'error');
        }
    }

    async loadWatchlist() {
        try {
            const response = await fetch(`${this.apiBase}/trading/watchlist`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.displayWatchlist(data.watchlist);
            }
        } catch (error) {
            console.error('Watchlist load error:', error);
        }
    }

    displayWatchlist(watchlist) {
        const container = document.getElementById('watchlistContainer');
        
        if (watchlist.length === 0) {
            container.innerHTML = '<div class="no-data">No stocks in watchlist. Add some from the trading section!</div>';
            return;
        }

        container.innerHTML = watchlist.map(stock => `
            <div class="watchlist-item">
                <div class="watchlist-header">
                    <div class="watchlist-symbol">${stock.symbol}</div>
                    <button onclick="app.removeFromWatchlist('${stock.symbol}')" class="remove-watchlist">Remove</button>
                </div>
                <div class="watchlist-name">${stock.name}</div>
                <div class="watchlist-price">${this.formatCurrency(stock.price)}</div>
                <div class="watchlist-change ${stock.change >= 0 ? 'text-success' : 'text-danger'}">
                    ${stock.change >= 0 ? '+' : ''}${this.formatCurrency(stock.change)} (${stock.changePercent.toFixed(2)}%)
                </div>
                <button onclick="app.selectStockForTrading('${stock.symbol}')" class="btn btn-sm mt-2">Trade</button>
            </div>
        `).join('');

        // Subscribe to price updates
        watchlist.forEach(stock => {
            this.socket.emit('subscribe_stock', { symbol: stock.symbol });
        });
    }

    async removeFromWatchlist(symbol) {
        try {
            const response = await fetch(`${this.apiBase}/trading/watchlist/${symbol}`, {
                method: 'DELETE',
                credentials: 'include'
            });

            const data = await response.json();
            if (data.success) {
                this.showToast(data.message, 'success');
                this.loadWatchlist();
            }
        } catch (error) {
            console.error('Remove watchlist error:', error);
        }
    }

    async loadTransactionHistory() {
        try {
            const response = await fetch(`${this.apiBase}/trading/transactions`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.displayTransactionHistory(data.transactions);
            }
        } catch (error) {
            console.error('Transaction history error:', error);
        }
    }

    displayTransactionHistory(transactions) {
        const tbody = document.getElementById('historyBody');
        
        if (transactions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="no-data">No transactions yet.</td></tr>';
            return;
        }

        tbody.innerHTML = transactions.map(tx => `
            <tr>
                <td>${new Date(tx.timestamp).toLocaleDateString()}</td>
                <td><strong>${tx.symbol}</strong></td>
                <td class="${tx.type === 'BUY' ? 'text-success' : 'text-danger'}">${tx.type}</td>
                <td>${tx.shares}</td>
                <td>${this.formatCurrency(tx.price)}</td>
                <td>${this.formatCurrency(tx.total_amount)}</td>
            </tr>
        `).join('');
    }

    handlePriceUpdate(data) {
        // Update stock info if it's the selected stock
        if (this.selectedStock && this.selectedStock.symbol === data.symbol) {
            this.selectedStock.price = data.price;
            document.getElementById('stockPrice').textContent = this.formatCurrency(data.price);
            this.updateTradeEstimate();
        }

        // Update portfolio holdings
        const holdingsRows = document.querySelectorAll('#holdingsBody tr');
        holdingsRows.forEach(row => {
            const symbolCell = row.querySelector('td:first-child strong');
            if (symbolCell && symbolCell.textContent === data.symbol) {
                const priceCell = row.querySelector('td:nth-child(4)');
                if (priceCell) {
                    priceCell.textContent = this.formatCurrency(data.price);
                }
            }
        });

        // Update watchlist
        const watchlistItems = document.querySelectorAll('.watchlist-item');
        watchlistItems.forEach(item => {
            const symbolEl = item.querySelector('.watchlist-symbol');
            if (symbolEl && symbolEl.textContent === data.symbol) {
                const priceEl = item.querySelector('.watchlist-price');
                if (priceEl) {
                    priceEl.textContent = this.formatCurrency(data.price);
                }
            }
        });
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        document.getElementById('toastContainer').appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    async loadAIRecommendations() {
        try {
            const response = await fetch(`${this.apiBase}/ai/recommendations`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.displayAIRecommendations(data.recommendations);
            } else {
                document.getElementById('aiRecommendations').innerHTML = '<div class="no-data">Unable to load AI recommendations</div>';
            }
        } catch (error) {
            console.error('AI recommendations error:', error);
            document.getElementById('aiRecommendations').innerHTML = '<div class="no-data">AI recommendations unavailable</div>';
        }
    }

    displayAIRecommendations(recommendations) {
        const container = document.getElementById('aiRecommendations');
        
        if (recommendations.length === 0) {
            container.innerHTML = '<div class="no-data">No AI recommendations available</div>';
            return;
        }

        container.innerHTML = recommendations.map(rec => `
            <div class="recommendation-card" onclick="app.selectStock('${rec.symbol}')">
                <div class="rec-header">
                    <div class="rec-symbol">${rec.symbol}</div>
                    <div class="rec-recommendation ${rec.recommendation}">${rec.recommendation}</div>
                </div>
                <div class="rec-change ${rec.trend_change >= 0 ? 'positive' : 'negative'}">
                    ${rec.trend_change >= 0 ? '+' : ''}${rec.trend_change.toFixed(2)}%
                </div>
                <div class="rec-confidence">Confidence: ${rec.confidence}</div>
            </div>
        `).join('');
    }

    async getAIPrediction() {
        if (!this.selectedStock) {
            this.showToast('Please select a stock first', 'warning');
            return;
        }

        const predictionBtn = document.getElementById('getPredictionBtn');
        predictionBtn.textContent = '🤖 Analyzing...';
        predictionBtn.disabled = true;

        try {
            const response = await fetch(`${this.apiBase}/ai/predict/${this.selectedStock.symbol}`, {
                credentials: 'include'
            });

            const data = await response.json();

            if (data.success) {
                this.displayAIPrediction(data.prediction);
                this.showToast('AI prediction generated', 'success');
            } else {
                this.showToast(data.message, 'error');
            }
        } catch (error) {
            console.error('AI prediction error:', error);
            this.showToast('AI prediction failed', 'error');
        } finally {
            predictionBtn.textContent = '🤖 Get AI Prediction';
            predictionBtn.disabled = false;
        }
    }

    displayAIPrediction(prediction) {
        document.getElementById('predictionRecommendation').textContent = prediction.recommendation;
        document.getElementById('predictionRecommendation').className = `recommendation ${prediction.recommendation}`;
        
        const changeEl = document.getElementById('predictionChange');
        changeEl.textContent = `${prediction.trend_change >= 0 ? '+' : ''}${prediction.trend_change.toFixed(2)}%`;
        changeEl.className = `change ${prediction.trend_change >= 0 ? 'positive' : 'negative'}`;
        
        document.getElementById('predictionConfidence').textContent = prediction.confidence;
        
        const predictionText = `AI predicts ${prediction.symbol} will ${prediction.trend_change >= 0 ? 'rise' : 'fall'} to $${prediction.predicted_price.toFixed(2)} over ${prediction.prediction_days} days.`;
        document.getElementById('predictionText').textContent = predictionText;
        
        document.getElementById('aiPrediction').style.display = 'block';
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }
}

// Initialize the app
const app = new StockTradingApp();