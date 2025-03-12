// YOLO Terminal Web Interface JavaScript

// Custom terminal-style alert function
function terminalAlert(message) {
    // Get popup elements
    const popup = document.getElementById('terminal-popup');
    const popupMessage = document.getElementById('terminal-popup-message');
    const popupOkBtn = document.getElementById('terminal-popup-ok-btn');
    
    // Set message
    popupMessage.textContent = message;
    
    // Show popup
    popup.classList.remove('hidden');
    
    // Focus OK button
    popupOkBtn.focus();
    
    // Return a promise that resolves when the OK button is clicked
    return new Promise(resolve => {
        popupOkBtn.onclick = () => {
            popup.classList.add('hidden');
            resolve();
        };
    });
}

// Custom terminal-style confirm function
function terminalConfirm(message) {
    // Create a custom confirm popup
    const popup = document.createElement('div');
    popup.className = 'terminal-popup';
    
    // Create popup content
    const popupContent = document.createElement('div');
    popupContent.className = 'terminal-popup-content';
    
    // Create popup header
    const popupHeader = document.createElement('div');
    popupHeader.className = 'terminal-popup-header';
    const popupTitle = document.createElement('h3');
    popupTitle.textContent = 'CONFIRM ACTION';
    popupHeader.appendChild(popupTitle);
    
    // Create popup body
    const popupBody = document.createElement('div');
    popupBody.className = 'terminal-popup-body';
    const popupMessage = document.createElement('p');
    popupMessage.textContent = message;
    popupBody.appendChild(popupMessage);
    
    // Create popup footer with Yes/No buttons
    const popupFooter = document.createElement('div');
    popupFooter.className = 'terminal-popup-footer';
    
    const yesBtn = document.createElement('button');
    yesBtn.textContent = 'YES';
    yesBtn.style.marginRight = '10px';
    
    const noBtn = document.createElement('button');
    noBtn.textContent = 'NO';
    
    popupFooter.appendChild(yesBtn);
    popupFooter.appendChild(noBtn);
    
    // Assemble popup
    popupContent.appendChild(popupHeader);
    popupContent.appendChild(popupBody);
    popupContent.appendChild(popupFooter);
    popup.appendChild(popupContent);
    
    // Add to document
    document.body.appendChild(popup);
    
    // Focus Yes button
    yesBtn.focus();
    
    // Return a promise that resolves with true or false
    return new Promise(resolve => {
        yesBtn.onclick = () => {
            document.body.removeChild(popup);
            resolve(true);
        };
        
        noBtn.onclick = () => {
            document.body.removeChild(popup);
            resolve(false);
        };
    });
}

// Override the default alert and confirm functions
window.originalAlert = window.alert;
window.originalConfirm = window.confirm;
window.alert = terminalAlert;
window.confirm = terminalConfirm;

// Game state
let gameState = {
    gameId: null,
    token: null,  // Add token property
    player: null,
    availableStocks: [],
    portfolio: [],
    headline: null,
    newsReports: [],
    message: "",
    netWorthHistory: [],
    selectedStock: null,
    selectedPortfolioStock: null,
    newsShown: false  // Flag to track if news has been shown for the current day
};

// DOM Elements
const elements = {
    // Screens
    welcomeScreen: document.getElementById('welcome-screen'),
    storyScreen: document.getElementById('story-screen'),
    gameScreen: document.getElementById('game-screen'),
    
    // Welcome Screen
    playerNameInput: document.getElementById('player-name'),
    startGameBtn: document.getElementById('start-game-btn'),
    viewStoryBtn: document.getElementById('view-story-btn'),
    backToWelcomeBtn: document.getElementById('back-to-welcome-btn'),
    
    // Game Screen - Status
    playerNameDisplay: document.getElementById('player-name-display'),
    daysLeft: document.getElementById('days-left'),
    currentDay: document.getElementById('current-day'),
    cash: document.getElementById('cash'),
    bankSavings: document.getElementById('bank-savings'),
    debt: document.getElementById('debt'),
    health: document.getElementById('health'),
    fame: document.getElementById('fame'),
    portfolioUsed: document.getElementById('portfolio-used'),
    portfolioCapacity: document.getElementById('portfolio-capacity'),
    portfolioDisplay: document.getElementById('portfolio-display'),
    portfolioItems: document.getElementById('portfolio-items'),
    headline: document.getElementById('headline'),
    
    // Game Screen - Content
    messageDisplay: document.getElementById('message-display'),
    newsReports: document.getElementById('news-reports'),
    newsContent: document.getElementById('news-content'),
    closeNewsBtn: document.getElementById('close-news-btn'),
    availableStocks: document.getElementById('available-stocks'),
    stocksList: document.getElementById('stocks-list'),
    closeStocksBtn: document.getElementById('close-stocks-btn'),
    
    // Main Menu
    mainMenu: document.getElementById('main-menu'),
    menuBtns: document.querySelectorAll('.menu-btn'),
    
    // Buy Stocks
    buyStocks: document.getElementById('buy-stocks'),
    buyStocksList: document.getElementById('buy-stocks-list'),
    buyControls: document.querySelector('.buy-controls'),
    buyAmount: document.getElementById('buy-amount'),
    confirmBuyBtn: document.getElementById('confirm-buy-btn'),
    cancelBuyBtn: document.getElementById('cancel-buy-btn'),
    backFromBuyBtn: document.getElementById('back-from-buy-btn'),
    
    // Sell Stocks
    sellStocks: document.getElementById('sell-stocks'),
    sellStocksList: document.getElementById('sell-stocks-list'),
    sellControls: document.querySelector('.sell-controls'),
    sellAmount: document.getElementById('sell-amount'),
    confirmSellBtn: document.getElementById('confirm-sell-btn'),
    cancelSellBtn: document.getElementById('cancel-sell-btn'),
    backFromSellBtn: document.getElementById('back-from-sell-btn'),
    
    // Bank
    bank: document.getElementById('bank'),
    bankCash: document.getElementById('bank-cash'),
    bankSavingsDisplay: document.getElementById('bank-savings-display'),
    bankDebt: document.getElementById('bank-debt'),
    depositAmount: document.getElementById('deposit-amount'),
    withdrawAmount: document.getElementById('withdraw-amount'),
    repayAmount: document.getElementById('repay-amount'),
    depositBtn: document.getElementById('deposit-btn'),
    withdrawBtn: document.getElementById('withdraw-btn'),
    repayBtn: document.getElementById('repay-btn'),
    backFromBankBtn: document.getElementById('back-from-bank-btn'),
    
    // Hospital
    hospital: document.getElementById('hospital'),
    hospitalHealth: document.getElementById('hospital-health'),
    hospitalCost: document.getElementById('hospital-cost'),
    healCost: document.getElementById('heal-cost'),
    healBtn: document.getElementById('heal-btn'),
    backFromHospitalBtn: document.getElementById('back-from-hospital-btn'),
    
    // Broker
    broker: document.getElementById('broker'),
    brokerDebt: document.getElementById('broker-debt'),
    brokerRepayAmount: document.getElementById('broker-repay-amount'),
    brokerRepayBtn: document.getElementById('broker-repay-btn'),
    backFromBrokerBtn: document.getElementById('back-from-broker-btn'),
    
    // Trading App
    tradingApp: document.getElementById('trading-app'),
    tradingAppCapacity: document.getElementById('trading-app-capacity'),
    upgradeBtn: document.getElementById('upgrade-btn'),
    backFromTradingAppBtn: document.getElementById('back-from-trading-app-btn'),
    
    // Darkweb
    darkweb: document.getElementById('darkweb'),
    darkwebVisits: document.getElementById('darkweb-visits'),
    darkwebBtn: document.getElementById('darkweb-btn'),
    backFromDarkwebBtn: document.getElementById('back-from-darkweb-btn'),
    
    // High Scores
    highScores: document.getElementById('high-scores'),
    highScoresList: document.getElementById('high-scores-list'),
    backFromHighScoresBtn: document.getElementById('back-from-high-scores-btn'),
    
    // Help
    help: document.getElementById('help'),
    backFromHelpBtn: document.getElementById('back-from-help-btn'),
    
    // Game Over
    gameOver: document.getElementById('game-over'),
    gameOverMessage: document.getElementById('game-over-message'),
    gameOverHighScores: document.getElementById('game-over-high-scores'),
    netWorthChart: document.getElementById('net-worth-chart'),
    newGameBtn: document.getElementById('new-game-btn'),
    
    // Chart Screen
    chartScreen: document.getElementById('chart-screen'),
    chartContainer: document.getElementById('chart-container'),
    shareTwitterBtn: document.getElementById('share-twitter'),
    shareLinkedInBtn: document.getElementById('share-linkedin'),
    backFromChartBtn: document.getElementById('back-from-chart-btn')
};

// API Functions
const api = {
    // Create a new game
    newGame: async (playerName) => {
        try {
            const response = await fetch('/api/new_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ player_name: playerName })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to create new game');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error creating new game:', error);
            alert('Error creating new game: ' + error.message);
            return null;
        }
    },
    
    // Get game state
    getGame: async (gameId) => {
        try {
            const response = await fetch(`/api/game/${gameId}`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to get game state');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting game state:', error);
            alert('Error getting game state: ' + error.message);
            return null;
        }
    },
    
    // Next day
    nextDay: async (gameId) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/next_day`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to advance to next day');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error advancing to next day:', error);
            alert('Error advancing to next day: ' + error.message);
            return null;
        }
    },
    
    // Buy stocks
    buyStocks: async (gameId, stockId, amount) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/buy`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ stock_id: stockId, amount: amount })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to buy stocks');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error buying stocks:', error);
            alert('Error buying stocks: ' + error.message);
            return null;
        }
    },
    
    // Sell stocks
    sellStocks: async (gameId, stockId, amount) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/sell`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ stock_id: stockId, amount: amount })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to sell stocks');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error selling stocks:', error);
            alert('Error selling stocks: ' + error.message);
            return null;
        }
    },
    
    // Bank actions
    bankAction: async (gameId, action, amount) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/bank`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action: action, amount: amount })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to perform bank action');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error performing bank action:', error);
            alert('Error performing bank action: ' + error.message);
            return null;
        }
    },
    
    // Hospital action
    hospitalAction: async (gameId) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/hospital`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to visit hospital');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error visiting hospital:', error);
            alert('Error visiting hospital: ' + error.message);
            return null;
        }
    },
    
    // Broker action
    brokerAction: async (gameId, amount) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/broker`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ amount: amount })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to visit broker');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error visiting broker:', error);
            alert('Error visiting broker: ' + error.message);
            return null;
        }
    },
    
    // Trading app action
    tradingAppAction: async (gameId) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/trading_app`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to use trading app');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error using trading app:', error);
            alert('Error using trading app: ' + error.message);
            return null;
        }
    },
    
    // Darkweb action
    darkwebAction: async (gameId) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/darkweb`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to visit darkweb');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error visiting darkweb:', error);
            alert('Error visiting darkweb: ' + error.message);
            return null;
        }
    },
    
    // Get high scores
    getHighScores: async () => {
        try {
            const response = await fetch('/api/high_scores');
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to get high scores');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting high scores:', error);
            alert('Error getting high scores: ' + error.message);
            return [];
        }
    },
    
    // Get chart data
    getChartData: async (gameId) => {
        try {
            // Use token if available, otherwise use gameId
            const idToUse = gameState.token || gameId;
            
            const response = await fetch(`/api/game/${idToUse}/chart`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to get chart data');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting chart data:', error);
            alert('Error getting chart data: ' + error.message);
            return null;
        }
    }
};

// UI Functions
const ui = {
    // Show screen
    showScreen: (screenId) => {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.add('hidden');
        });
        document.getElementById(screenId).classList.remove('hidden');
    },
    
    // Show action screen
    showActionScreen: (screenId) => {
        document.querySelectorAll('.action-screen').forEach(screen => {
            screen.classList.add('hidden');
        });
        elements.mainMenu.classList.add('hidden');
        document.getElementById(screenId).classList.remove('hidden');
    },
    
    // Show main menu
    showMainMenu: () => {
        document.querySelectorAll('.action-screen').forEach(screen => {
            screen.classList.add('hidden');
        });
        elements.mainMenu.classList.remove('hidden');
    },
    
    // Update player status
    updatePlayerStatus: () => {
        const player = gameState.player;
        
        elements.playerNameDisplay.textContent = player.name;
        elements.daysLeft.textContent = player.days_left;
        elements.currentDay.textContent = gameState.current_day || '';
        elements.cash.textContent = player.cash;
        elements.bankSavings.textContent = player.bank_savings;
        
        // Set color for debt - bold red if not zero, normal color otherwise
        if (player.debt > 0) {
            elements.debt.className = 'debt-warning'; // Bold red class
        } else {
            elements.debt.className = ''; // Normal color
        }
        elements.debt.textContent = player.debt;
        
        // Set color for health
        if (player.health > 50) {
            elements.health.className = 'positive';
        } else if (player.health > 25) {
            elements.health.className = 'highlight';
        } else {
            elements.health.className = 'negative';
        }
        elements.health.textContent = player.health;
        
        // Set color for fame
        if (player.fame > 50) {
            elements.fame.className = 'positive';
        } else if (player.fame > 25) {
            elements.fame.className = 'highlight';
        } else {
            elements.fame.className = 'negative';
        }
        elements.fame.textContent = player.fame;
        
        // Set color for portfolio
        if (player.portfolio_used < player.portfolio_capacity * 0.8) {
            elements.portfolioUsed.className = 'positive';
        } else if (player.portfolio_used < player.portfolio_capacity * 0.95) {
            elements.portfolioUsed.className = 'highlight';
        } else {
            elements.portfolioUsed.className = 'negative';
        }
        elements.portfolioUsed.textContent = player.portfolio_used;
        elements.portfolioCapacity.textContent = player.portfolio_capacity;
        
        // Update portfolio display
        ui.updatePortfolio();
        
        // Update headline with colored agency name
        if (gameState.headline) {
            const agency = gameState.headline.agency;
            const agencyClass = getAgencyColorClass(agency);
            const headlineText = `[<span class="${agencyClass}">${agency}</span>] ${gameState.headline.text}`;
            elements.headline.innerHTML = headlineText;
        }
    },
    
    // Update portfolio display
    updatePortfolio: () => {
        elements.portfolioItems.innerHTML = '';
        
        if (gameState.portfolio.length === 0) {
            elements.portfolioDisplay.classList.add('hidden');
            return;
        }
        
        elements.portfolioDisplay.classList.remove('hidden');
        
        gameState.portfolio.forEach(stock => {
            const item = document.createElement('div');
            item.className = 'portfolio-item';
            
            // Determine if stock is cryptocurrency
            const isCrypto = ['CATO', 'PITCOIN'].includes(stock.ticker);
            const tickerClass = isCrypto ? 'crypto' : 'stock';
            
            // Determine if stock is profitable
            const isProfitable = stock.market_price > stock.price;
            const priceClass = isProfitable ? 'positive' : (stock.market_price > 0 ? 'highlight' : '');
            
            // Create HTML for portfolio item
            let html = `<span class="${tickerClass}">$${stock.ticker}</span> (${stock.name}) - Qty: ${stock.quantity} - `;
            html += `<span class="${priceClass}">Cost basis: $${stock.price}</span>`;
            
            if (stock.market_price > 0) {
                const profit = stock.market_price - stock.price;
                const profitClass = profit > 0 ? 'positive' : 'negative';
                const profitSign = profit > 0 ? '+' : '';
                html += ` - Current: $${stock.market_price} (<span class="${profitClass}">${profitSign}$${profit}</span>)`;
            }
            
            item.innerHTML = html;
            elements.portfolioItems.appendChild(item);
        });
    },
    
    // Show message
    showMessage: (message) => {
        elements.messageDisplay.textContent = message;
    },
    
    // Show news reports
    showNewsReports: () => {
        if (!gameState.newsReports || gameState.newsReports.length === 0) {
            return;
        }
        
        elements.newsContent.innerHTML = '';
        
        gameState.newsReports.forEach(report => {
            const item = document.createElement('div');
            item.className = 'news-item';
            item.textContent = report;
            elements.newsContent.appendChild(item);
        });
        
        elements.newsReports.classList.remove('hidden');
        elements.mainMenu.classList.add('hidden');
    },
    
    // Show available stocks
    showAvailableStocks: () => {
        elements.stocksList.innerHTML = '';
        
        if (gameState.availableStocks.length === 0) {
            const item = document.createElement('div');
            item.textContent = 'No stocks available for trading today.';
            elements.stocksList.appendChild(item);
        } else {
            gameState.availableStocks.forEach((stock, index) => {
                const item = document.createElement('div');
                item.className = 'stock-item';
                item.dataset.id = stock.id;
                
                // Determine if stock is cryptocurrency
                const isCrypto = ['CATO', 'PITCOIN'].includes(stock.ticker);
                const tickerClass = isCrypto ? 'crypto' : 'stock';
                
                item.innerHTML = `${index + 1}. <span class="${tickerClass}">$${stock.ticker}</span> (${stock.name}) - Price: $${stock.price}`;
                elements.stocksList.appendChild(item);
            });
        }
        
        elements.availableStocks.classList.remove('hidden');
        elements.mainMenu.classList.add('hidden');
    },
    
    // Show buy stocks
    showBuyStocks: () => {
        elements.buyStocksList.innerHTML = '';
        
        if (gameState.availableStocks.length === 0) {
            const item = document.createElement('div');
            item.textContent = 'No stocks available for trading today.';
            elements.buyStocksList.appendChild(item);
        } else {
            gameState.availableStocks.forEach((stock, index) => {
                const item = document.createElement('div');
                item.className = 'stock-item';
                item.dataset.id = stock.id;
                
                // Determine if stock is cryptocurrency
                const isCrypto = ['CATO', 'PITCOIN'].includes(stock.ticker);
                const tickerClass = isCrypto ? 'crypto' : 'stock';
                
                item.innerHTML = `${index + 1}. <span class="${tickerClass}">$${stock.ticker}</span> (${stock.name}) - Price: $${stock.price}`;
                
                // Add click event
                item.addEventListener('click', () => {
                    // Remove selected class from all items
                    document.querySelectorAll('.stock-item').forEach(item => {
                        item.classList.remove('selected');
                    });
                    
                    // Add selected class to clicked item
                    item.classList.add('selected');
                    
                    // Set selected stock
                    gameState.selectedStock = stock;
                    
                    // Calculate max amount player can buy
                    const maxBuy = Math.min(
                        Math.floor(gameState.player.cash / stock.price),
                        gameState.player.portfolio_capacity - gameState.player.portfolio_used
                    );
                    
                    if (maxBuy <= 0) {
                        alert("You don't have enough space in your trade book or cash to buy this stock.");
                        return;
                    }
                    
                    // Show buy controls
                    elements.buyAmount.value = 1;
                    elements.buyAmount.max = maxBuy;
                    elements.buyControls.classList.remove('hidden');
                });
                
                elements.buyStocksList.appendChild(item);
            });
        }
        
        // Hide buy controls
        elements.buyControls.classList.add('hidden');
        
        ui.showActionScreen('buy-stocks');
    },
    
    // Show sell stocks
    showSellStocks: () => {
        elements.sellStocksList.innerHTML = '';
        
        if (gameState.portfolio.length === 0) {
            const item = document.createElement('div');
            item.textContent = "You don't have any stocks to sell.";
            elements.sellStocksList.appendChild(item);
        } else {
            gameState.portfolio.forEach((stock, index) => {
                const item = document.createElement('div');
                item.className = 'stock-item';
                item.dataset.id = stock.id;
                
                // Determine if stock is cryptocurrency
                const isCrypto = ['CATO', 'PITCOIN'].includes(stock.ticker);
                const tickerClass = isCrypto ? 'crypto' : 'stock';
                
                // Create HTML for sell item
                let html = `${index + 1}. <span class="${tickerClass}">$${stock.ticker}</span> (${stock.name}) - Qty: ${stock.quantity} - Bought: $${stock.price}`;
                
                // Check if stock is available in market
                if (stock.market_price > 0) {
                    const profit = stock.market_price - stock.price;
                    const profitClass = profit > 0 ? 'positive' : 'negative';
                    const profitSign = profit > 0 ? '+' : '';
                    html += ` - Current: $${stock.market_price} (<span class="${profitClass}">${profitSign}$${profit}</span>)`;
                } else {
                    html += ' (Not tradable now)';
                }
                
                item.innerHTML = html;
                
                // Add click event only if stock is tradable
                if (stock.market_price > 0) {
                    item.addEventListener('click', () => {
                        // Remove selected class from all items
                        document.querySelectorAll('.stock-item').forEach(item => {
                            item.classList.remove('selected');
                        });
                        
                        // Add selected class to clicked item
                        item.classList.add('selected');
                        
                        // Set selected portfolio stock
                        gameState.selectedPortfolioStock = stock;
                        
                        // Show sell controls
                        elements.sellAmount.value = 1;
                        elements.sellAmount.max = stock.quantity;
                        elements.sellControls.classList.remove('hidden');
                    });
                }
                
                elements.sellStocksList.appendChild(item);
            });
        }
        
        // Hide sell controls
        elements.sellControls.classList.add('hidden');
        
        ui.showActionScreen('sell-stocks');
    },
    
    // Show bank
    showBank: () => {
        elements.bankCash.textContent = gameState.player.cash;
        elements.bankSavingsDisplay.textContent = gameState.player.bank_savings;
        elements.bankDebt.textContent = gameState.player.debt;
        
        // Calculate the maximum amount that can be repaid
        const maxRepay = Math.min(gameState.player.cash, gameState.player.debt);
        
        // Set default values
        elements.depositAmount.value = Math.min(100, gameState.player.cash);
        elements.withdrawAmount.value = Math.min(100, gameState.player.bank_savings);
        elements.repayAmount.value = maxRepay; // Set to max repay amount
        
        // Set max values
        elements.depositAmount.max = gameState.player.cash;
        elements.withdrawAmount.max = gameState.player.bank_savings;
        elements.repayAmount.max = maxRepay;
        
        ui.showActionScreen('bank');
    },
    
    // Show hospital
    showHospital: () => {
        elements.hospitalHealth.textContent = gameState.player.health;
        
        // Calculate cost
        const copay = 200;
        const healthNeeded = 100 - gameState.player.health;
        const healthCost = healthNeeded * 10000;  // $10,000 per health point
        const totalCost = copay + healthCost;
        
        elements.hospitalCost.textContent = totalCost;
        elements.healCost.textContent = totalCost;
        
        // Set up heal button
        if (healthNeeded === 0 || gameState.player.cash < totalCost) {
            elements.healBtn.disabled = true;
            
            // Add click event to show message when disabled
            elements.healBtn.onclick = () => {
                if (healthNeeded === 0) {
                    alert("You already have full health!");
                } else if (gameState.player.cash < totalCost) {
                    alert(`You don't have enough cash! You need $${totalCost} but only have $${gameState.player.cash}.`);
                }
            };
        } else {
            elements.healBtn.disabled = false;
            // Remove the onclick event when the button is enabled
            elements.healBtn.onclick = null;
        }
        
        ui.showActionScreen('hospital');
    },
    
    // Show broker
    showBroker: () => {
        elements.brokerDebt.textContent = gameState.player.debt;
        
        // Calculate the maximum amount that can be repaid
        const maxRepay = Math.min(gameState.player.cash, gameState.player.debt);
        
        // Set default value to the maximum amount that can be repaid
        // This way the player can pay off their debt in one click if they have enough cash
        elements.brokerRepayAmount.value = maxRepay;
        
        // Set max value
        elements.brokerRepayAmount.max = maxRepay;
        
        // Disable repay button if player has no debt or not enough cash
        if (gameState.player.debt === 0 || gameState.player.cash === 0) {
            elements.brokerRepayBtn.disabled = true;
        } else {
            elements.brokerRepayBtn.disabled = false;
        }
        
        ui.showActionScreen('broker');
    },
    
    // Show trading app
    showTradingApp: () => {
        elements.tradingAppCapacity.textContent = gameState.player.portfolio_capacity;
        
        // Set up upgrade button
        if (gameState.player.cash < 30000) {
            elements.upgradeBtn.disabled = true;
            
            // Add click event to show message when disabled
            elements.upgradeBtn.onclick = () => {
                alert(`You don't have enough cash! You need $30,000 but only have $${gameState.player.cash}.`);
            };
        } else {
            elements.upgradeBtn.disabled = false;
            // Remove the onclick event when the button is enabled
            elements.upgradeBtn.onclick = null;
        }
        
        ui.showActionScreen('trading-app');
    },
    
    // Show darkweb
    showDarkweb: () => {
        elements.darkwebVisits.textContent = gameState.player.darkweb_visits || 0;
        
        // Disable darkweb button if player has visited too many times
        if ((gameState.player.darkweb_visits || 0) >= 3) {
            elements.darkwebBtn.disabled = true;
        } else {
            elements.darkwebBtn.disabled = false;
        }
        
        ui.showActionScreen('darkweb');
    },
    
    // Show high scores
    showHighScores: async () => {
        const highScores = await api.getHighScores();
        
        elements.highScoresList.innerHTML = '';
        
        if (highScores.length === 0) {
            elements.highScoresList.textContent = 'No high scores yet.';
        } else {
            const table = document.createElement('table');
            
            // Create table header
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            ['Rank', 'Name', 'Score', 'Health', 'Rep'].forEach(text => {
                const th = document.createElement('th');
                th.textContent = text;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);
            
            // Create table body
            const tbody = document.createElement('tbody');
            highScores.forEach((score, index) => {
                const row = document.createElement('tr');
                
                // Rank
                const rankCell = document.createElement('td');
                rankCell.textContent = index + 1;
                row.appendChild(rankCell);
                
                // Name
                const nameCell = document.createElement('td');
                nameCell.textContent = score.name;
                row.appendChild(nameCell);
                
                // Score
                const scoreCell = document.createElement('td');
                scoreCell.textContent = '$' + score.score;
                row.appendChild(scoreCell);
                
                // Health
                const healthCell = document.createElement('td');
                healthCell.textContent = score.health;
                row.appendChild(healthCell);
                
                // Rep
                const repCell = document.createElement('td');
                repCell.textContent = score.fame;
                row.appendChild(repCell);
                
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
            
            elements.highScoresList.appendChild(table);
        }
        
        ui.showActionScreen('high-scores');
    },
    
    // Show help
    showHelp: () => {
        ui.showActionScreen('help');
    },
    
    // Show game over
    showGameOver: (gameOverData) => {
        // Hide main menu and other action screens
        document.querySelectorAll('.action-screen').forEach(screen => {
            screen.classList.add('hidden');
        });
        elements.mainMenu.classList.add('hidden');
        
        elements.gameOverMessage.innerHTML = gameState.message;
        
        // Show high scores
        elements.gameOverHighScores.innerHTML = '';
        
        if (gameOverData.high_scores && gameOverData.high_scores.length > 0) {
            const table = document.createElement('table');
            
            // Create table header
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            ['Rank', 'Name', 'Score', 'Health', 'Rep'].forEach(text => {
                const th = document.createElement('th');
                th.textContent = text;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);
            
            // Create table body
            const tbody = document.createElement('tbody');
            gameOverData.high_scores.forEach((score, index) => {
                const row = document.createElement('tr');
                
                // Highlight current player's score
                if (score.name === gameState.player.name && score.score === gameOverData.final_score) {
                    row.className = 'highlight';
                }
                
                // Rank
                const rankCell = document.createElement('td');
                rankCell.textContent = index + 1;
                row.appendChild(rankCell);
                
                // Name
                const nameCell = document.createElement('td');
                nameCell.textContent = score.name;
                row.appendChild(nameCell);
                
                // Score
                const scoreCell = document.createElement('td');
                scoreCell.textContent = '$' + score.score;
                row.appendChild(scoreCell);
                
                // Health
                const healthCell = document.createElement('td');
                healthCell.textContent = score.health;
                row.appendChild(healthCell);
                
                // Rep
                const repCell = document.createElement('td');
                repCell.textContent = score.fame;
                row.appendChild(repCell);
                
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
            
            elements.gameOverHighScores.appendChild(table);
        }
        
        // Show net worth chart
        if (gameState.netWorthHistory && gameState.netWorthHistory.length > 0) {
            elements.netWorthChart.innerHTML = '';
            
            // Create a chart container
            const chartContainer = document.createElement('div');
            chartContainer.className = 'chart-container';
            
            // Add chart title
            const chartTitle = document.createElement('h3');
            chartTitle.textContent = 'Net Worth History';
            chartContainer.appendChild(chartTitle);
            
            // Create canvas for chart
            const chartCanvas = document.createElement('canvas');
            chartCanvas.width = 600;
            chartCanvas.height = 300;
            chartContainer.appendChild(chartCanvas);
            
            // Draw chart
            const ctx = chartCanvas.getContext('2d');
            
            // Set background
            ctx.fillStyle = '#f5f5f5';
            ctx.fillRect(0, 0, chartCanvas.width, chartCanvas.height);
            
            // Draw grid
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            
            // Vertical grid lines
            for (let i = 0; i <= 10; i++) {
                const x = i * (chartCanvas.width / 10);
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, chartCanvas.height);
                ctx.stroke();
            }
            
            // Horizontal grid lines
            for (let i = 0; i <= 10; i++) {
                const y = i * (chartCanvas.height / 10);
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(chartCanvas.width, y);
                ctx.stroke();
            }
            
            // Find min and max values
            const netWorthValues = gameState.netWorthHistory.map(item => item.net_worth);
            const minNetWorth = Math.min(...netWorthValues);
            const maxNetWorth = Math.max(...netWorthValues);
            const range = maxNetWorth - minNetWorth;
            
            // Draw net worth line
            ctx.strokeStyle = '#007bff';
            ctx.lineWidth = 3;
            ctx.beginPath();
            
            gameState.netWorthHistory.forEach((item, index) => {
                const x = (index / (gameState.netWorthHistory.length - 1)) * chartCanvas.width;
                const y = chartCanvas.height - ((item.net_worth - minNetWorth) / range) * chartCanvas.height;
                
                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            
            ctx.stroke();
            
            // Add points
            ctx.fillStyle = '#007bff';
            gameState.netWorthHistory.forEach((item, index) => {
                const x = (index / (gameState.netWorthHistory.length - 1)) * chartCanvas.width;
                const y = chartCanvas.height - ((item.net_worth - minNetWorth) / range) * chartCanvas.height;
                
                ctx.beginPath();
                ctx.arc(x, y, 5, 0, Math.PI * 2);
                ctx.fill();
            });
            
            // Add labels
            ctx.fillStyle = '#333';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            
            // X-axis labels (days)
            for (let i = 0; i <= 40; i += 10) {
                const x = (i / 40) * chartCanvas.width;
                ctx.fillText(`Day ${i}`, x, chartCanvas.height - 10);
            }
            
            // Y-axis labels (net worth)
            ctx.textAlign = 'right';
            for (let i = 0; i <= 10; i++) {
                const y = i * (chartCanvas.height / 10);
                const value = maxNetWorth - (i / 10) * range;
                ctx.fillText(`$${Math.round(value)}`, 50, y + 5);
            }
            
            // Add chart description
            const chartDesc = document.createElement('p');
            chartDesc.textContent = `This chart shows your net worth over the 40-day trading period. You started with $2,000 in cash and $5,000 in debt, and ended with a final score of $${gameOverData.final_score}.`;
            chartContainer.appendChild(chartDesc);
            
            elements.netWorthChart.appendChild(chartContainer);
        }
        
        ui.showActionScreen('game-over');
    },
    
    // Draw net worth chart
    drawNetWorthChart: (netWorthHistory) => {
        // This is a placeholder for a more sophisticated chart
        // In a real implementation, you might use a library like Chart.js
        console.log('Drawing net worth chart with data:', netWorthHistory);
    },
    
    // Show chart screen
    showChartScreen: async (gameId) => {
        // Get chart data
        const chartData = await api.getChartData(gameId);
        
        if (!chartData) {
            return;
        }
        
        // Clear chart container
        elements.chartContainer.innerHTML = '';
        
        // Create chart title
        const chartTitle = document.createElement('h2');
        chartTitle.textContent = `${chartData.player_name}'s Trading Journey`;
        elements.chartContainer.appendChild(chartTitle);
        
        // Create chart subtitle
        const chartSubtitle = document.createElement('h3');
        chartSubtitle.textContent = `Final Score: $${chartData.final_score}`;
        elements.chartContainer.appendChild(chartSubtitle);
        
        // Create chart
        const chartDiv = document.createElement('div');
        chartDiv.className = 'net-worth-chart';
        
        // Create a simple chart visualization
        const chartCanvas = document.createElement('canvas');
        chartCanvas.width = 800;
        chartCanvas.height = 400;
        chartDiv.appendChild(chartCanvas);
        
        // Draw chart
        const ctx = chartCanvas.getContext('2d');
        
        // Set background
        ctx.fillStyle = '#f5f5f5';
        ctx.fillRect(0, 0, chartCanvas.width, chartCanvas.height);
        
        // Draw grid
        ctx.strokeStyle = '#ddd';
        ctx.lineWidth = 1;
        
        // Vertical grid lines
        for (let i = 0; i <= 10; i++) {
            const x = i * (chartCanvas.width / 10);
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, chartCanvas.height);
            ctx.stroke();
        }
        
        // Horizontal grid lines
        for (let i = 0; i <= 10; i++) {
            const y = i * (chartCanvas.height / 10);
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(chartCanvas.width, y);
            ctx.stroke();
        }
        
        // Find min and max values
        const netWorthValues = chartData.net_worth_history.map(item => item.net_worth);
        const minNetWorth = Math.min(...netWorthValues);
        const maxNetWorth = Math.max(...netWorthValues);
        const range = maxNetWorth - minNetWorth;
        
        // Draw net worth line
        ctx.strokeStyle = '#007bff';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        chartData.net_worth_history.forEach((item, index) => {
            const x = (index / (chartData.net_worth_history.length - 1)) * chartCanvas.width;
            const y = chartCanvas.height - ((item.net_worth - minNetWorth) / range) * chartCanvas.height;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Add points
        ctx.fillStyle = '#007bff';
        chartData.net_worth_history.forEach((item, index) => {
            const x = (index / (chartData.net_worth_history.length - 1)) * chartCanvas.width;
            const y = chartCanvas.height - ((item.net_worth - minNetWorth) / range) * chartCanvas.height;
            
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();
        });
        
        // Add labels
        ctx.fillStyle = '#333';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        
        // X-axis labels (days)
        for (let i = 0; i <= 40; i += 10) {
            const x = (i / 40) * chartCanvas.width;
            ctx.fillText(`Day ${i}`, x, chartCanvas.height - 10);
        }
        
        // Y-axis labels (net worth)
        ctx.textAlign = 'right';
        for (let i = 0; i <= 10; i++) {
            const y = i * (chartCanvas.height / 10);
            const value = maxNetWorth - (i / 10) * range;
            ctx.fillText(`$${Math.round(value)}`, 50, y + 5);
        }
        
        elements.chartContainer.appendChild(chartDiv);
        
        // Add chart description
        const chartDesc = document.createElement('p');
        chartDesc.textContent = `This chart shows your net worth over the 40-day trading period. You started with $2,000 in cash and $5,000 in debt, and ended with a final score of $${chartData.final_score}.`;
        elements.chartContainer.appendChild(chartDesc);
        
        // Show share buttons only if game is completed
        if (chartData.game_completed) {
            // Configure share buttons
            const shareUrl = window.location.href;
            const shareText = `I just finished YOLO Terminal with a score of $${chartData.final_score}! Check out my trading journey!`;
            
            // Twitter share
            elements.shareTwitterBtn.onclick = () => {
                const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`;
                window.open(twitterUrl, '_blank');
            };
            
            // LinkedIn share
            elements.shareLinkedInBtn.onclick = () => {
                const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`;
                window.open(linkedInUrl, '_blank');
            };
            
            // Show share buttons
            elements.shareTwitterBtn.style.display = 'inline-block';
            elements.shareLinkedInBtn.style.display = 'inline-block';
        } else {
            // Hide share buttons if game is not completed
            elements.shareTwitterBtn.style.display = 'none';
            elements.shareLinkedInBtn.style.display = 'none';
        }
        
        // Show chart screen
        ui.showScreen('chart-screen');
    }
};

// Game Functions
const game = {
    // Initialize game
    init: () => {
        // Check if there's a token in the URL
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        
        if (token) {
            // Try to load the game with the token
            api.getGame(token).then(async data => {
                if (data) {
                    game.loadGameState(data);
                    
                    // Check if game is completed (days_left <= 0 or health <= 0)
                    if (data.player.days_left <= 0 || data.player.health <= 0) {
                        // Show chart screen
                        await ui.showChartScreen(token);
                    } else {
                        // Show game screen
                        ui.showScreen('game-screen');
                    }
                } else {
                    // If the game couldn't be loaded, show the welcome screen
                    ui.showScreen('welcome-screen');
                }
            }).catch(error => {
                console.error('Error loading game with token:', error);
                ui.showScreen('welcome-screen');
            });
        } else {
            // No token, show the welcome screen
            ui.showScreen('welcome-screen');
        }
        
        // Add event listeners
        
        // Welcome screen
        elements.startGameBtn.addEventListener('click', async () => {
            const playerName = elements.playerNameInput.value.trim() || 'Trader';
            const data = await api.newGame(playerName);
            
            if (data) {
                // Update the URL with the token
                const newUrl = window.location.pathname + '?token=' + data.token;
                window.history.pushState({ path: newUrl }, '', newUrl);
                
                game.loadGameState(data);
                ui.showScreen('game-screen');
            }
        });
        
        elements.viewStoryBtn.addEventListener('click', () => {
            ui.showScreen('story-screen');
        });
        
        elements.backToWelcomeBtn.addEventListener('click', () => {
            ui.showScreen('welcome-screen');
        });
        
        // Main menu
        elements.menuBtns.forEach(btn => {
            btn.addEventListener('click', async () => {
                const action = btn.dataset.action;
                
                switch (action) {
                    case 'next_day':
                        const data = await api.nextDay(gameState.gameId);
                        
                        if (data) {
                            // Reset the newsShown flag when advancing to the next day
                            gameState.newsShown = false;
                            
                            game.loadGameState(data);
                            
                            // Check if game is over
                            if (data.game_over) {
                                // Show game over screen with net worth chart
                                ui.showGameOver(data);
                                
                                // Don't proceed to show news or stocks when game is over
                                return;
                            }
                            
                            // Only show news and stocks if game is not over
                            if (data.news_reports && data.news_reports.length > 0) {
                                ui.showNewsReports();
                            } else {
                                ui.showAvailableStocks();
                            }
                        }
                        break;
                    
                    case 'buy':
                        ui.showBuyStocks();
                        break;
                    
                    case 'sell':
                        ui.showSellStocks();
                        break;
                    
                    case 'bank':
                        ui.showBank();
                        break;
                    
                    case 'hospital':
                        ui.showHospital();
                        break;
                    
                    case 'broker':
                        ui.showBroker();
                        break;
                    
                    case 'trading_app':
                        ui.showTradingApp();
                        break;
                    
                    case 'darkweb':
                        ui.showDarkweb();
                        break;
                    
                    case 'high_scores':
                        ui.showHighScores();
                        break;
                    
                    case 'help':
                        ui.showHelp();
                        break;
                    
                    case 'quit':
                        // Use our custom confirm dialog
                        (async () => {
                            const confirmed = await confirm('Are you sure you want to quit?');
                            if (confirmed) {
                                ui.showScreen('welcome-screen');
                            }
                        })();
                        break;
                }
            });
        });
        
        // News reports
        elements.closeNewsBtn.addEventListener('click', () => {
            elements.newsReports.classList.add('hidden');
            
            // Show available stocks if flag is set
            if (gameState.showStocks) {
                // Clear the flag to prevent showing stocks again
                gameState.showStocks = false;
                
                // Show available stocks
                ui.showAvailableStocks();
            } else {
                ui.showMainMenu();
            }
        });
        
        // Available stocks
        elements.closeStocksBtn.addEventListener('click', () => {
            elements.availableStocks.classList.add('hidden');
            ui.showMainMenu();
        });
        
        // Buy stocks
        elements.maxBuyBtn = document.getElementById('max-buy-btn');
        elements.maxBuyBtn.addEventListener('click', () => {
            if (!gameState.selectedStock) {
                alert('Please select a stock to buy.');
                return;
            }
            
            // Calculate max amount player can buy
            const maxBuy = Math.min(
                Math.floor(gameState.player.cash / gameState.selectedStock.price),
                gameState.player.portfolio_capacity - gameState.player.portfolio_used
            );
            
            elements.buyAmount.value = maxBuy;
        });
        
        // Add input validation to ensure integers
        elements.buyAmount.addEventListener('input', () => {
            // Remove any non-digit characters
            elements.buyAmount.value = elements.buyAmount.value.replace(/\D/g, '');
            
            // Ensure it's not empty
            if (elements.buyAmount.value === '') {
                elements.buyAmount.value = '1';
            }
            
            // Ensure it's within min/max range
            const value = parseInt(elements.buyAmount.value);
            const max = parseInt(elements.buyAmount.max);
            if (value > max) {
                elements.buyAmount.value = max.toString();
            }
        });
        
        elements.confirmBuyBtn.addEventListener('click', async () => {
            if (!gameState.selectedStock) {
                alert('Please select a stock to buy.');
                return;
            }
            
            const amount = parseInt(elements.buyAmount.value);
            
            if (isNaN(amount) || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }
            
            const data = await api.buyStocks(gameState.gameId, gameState.selectedStock.id, amount);
            
            if (data) {
                // Clear the show_stocks flag to prevent showing stocks again
                data.show_stocks = false;
                game.loadGameState(data);
                ui.showMainMenu();
            }
        });
        
        elements.cancelBuyBtn.addEventListener('click', () => {
            elements.buyControls.classList.add('hidden');
            gameState.selectedStock = null;
            
            // Remove selected class from all items
            document.querySelectorAll('.stock-item').forEach(item => {
                item.classList.remove('selected');
            });
        });
        
        elements.backFromBuyBtn.addEventListener('click', () => {
            ui.showMainMenu();
        });
        
        // Sell stocks
        elements.maxSellBtn = document.getElementById('max-sell-btn');
        elements.maxSellBtn.addEventListener('click', () => {
            if (!gameState.selectedPortfolioStock) {
                alert('Please select a stock to sell.');
                return;
            }
            
            // Set to max quantity
            elements.sellAmount.value = gameState.selectedPortfolioStock.quantity;
        });
        
        // Add input validation to ensure integers
        elements.sellAmount.addEventListener('input', () => {
            // Remove any non-digit characters
            elements.sellAmount.value = elements.sellAmount.value.replace(/\D/g, '');
            
            // Ensure it's not empty
            if (elements.sellAmount.value === '') {
                elements.sellAmount.value = '1';
            }
            
            // Ensure it's within min/max range
            const value = parseInt(elements.sellAmount.value);
            const max = parseInt(elements.sellAmount.max);
            if (value > max) {
                elements.sellAmount.value = max.toString();
            }
        });
        
        elements.confirmSellBtn.addEventListener('click', async () => {
            if (!gameState.selectedPortfolioStock) {
                alert('Please select a stock to sell.');
                return;
            }
            
            const amount = parseInt(elements.sellAmount.value);
            
            if (isNaN(amount) || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }
            
            const data = await api.sellStocks(gameState.gameId, gameState.selectedPortfolioStock.id, amount);
            
            if (data) {
                // Clear the show_stocks flag to prevent showing stocks again
                data.show_stocks = false;
                game.loadGameState(data);
                ui.showMainMenu();
            }
        });
        
        elements.cancelSellBtn.addEventListener('click', () => {
            elements.sellControls.classList.add('hidden');
            gameState.selectedPortfolioStock = null;
            
            // Remove selected class from all items
            document.querySelectorAll('.stock-item').forEach(item => {
                item.classList.remove('selected');
            });
        });
        
        elements.backFromSellBtn.addEventListener('click', () => {
            ui.showMainMenu();
        });
        
        // Bank
        // Add input validation to ensure integers for deposit amount
        elements.depositAmount.addEventListener('input', () => {
            // Remove any non-digit characters
            elements.depositAmount.value = elements.depositAmount.value.replace(/\D/g, '');
            
            // Ensure it's not empty
            if (elements.depositAmount.value === '') {
                elements.depositAmount.value = '1';
            }
            
            // Ensure it's within min/max range
            const value = parseInt(elements.depositAmount.value);
            const max = parseInt(elements.depositAmount.max);
            if (value > max) {
                elements.depositAmount.value = max.toString();
            }
        });
        
        // Add input validation to ensure integers for withdraw amount
        elements.withdrawAmount.addEventListener('input', () => {
            // Remove any non-digit characters
            elements.withdrawAmount.value = elements.withdrawAmount.value.replace(/\D/g, '');
            
            // Ensure it's not empty
            if (elements.withdrawAmount.value === '') {
                elements.withdrawAmount.value = '1';
            }
            
            // Ensure it's within min/max range
            const value = parseInt(elements.withdrawAmount.value);
            const max = parseInt(elements.withdrawAmount.max);
            if (value > max) {
                elements.withdrawAmount.value = max.toString();
            }
        });
        
        // Add input validation to ensure integers for repay amount
        elements.repayAmount.addEventListener('input', () => {
            // Remove any non-digit characters
            elements.repayAmount.value = elements.repayAmount.value.replace(/\D/g, '');
            
            // Ensure it's not empty
            if (elements.repayAmount.value === '') {
                elements.repayAmount.value = '1';
            }
            
            // Ensure it's within min/max range
            const value = parseInt(elements.repayAmount.value);
            const max = parseInt(elements.repayAmount.max);
            if (value > max) {
                elements.repayAmount.value = max.toString();
            }
        });
        
        elements.depositBtn.addEventListener('click', async () => {
            const amount = parseInt(elements.depositAmount.value);
            
            if (isNaN(amount) || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }
            
            const data = await api.bankAction(gameState.gameId, 'deposit', amount);
            
            if (data) {
                // Clear the show_stocks flag to prevent showing stocks again
                data.show_stocks = false;
                game.loadGameState(data);
                ui.showBank();
            }
        });
        
        elements.withdrawBtn.addEventListener('click', async () => {
            const amount = parseInt(elements.withdrawAmount.value);
            
            if (isNaN(amount) || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }
            
            const data = await api.bankAction(gameState.gameId, 'withdraw', amount);
            
            if (data) {
                // Clear the show_stocks flag to prevent showing stocks again
                data.show_stocks = false;
                game.loadGameState(data);
                ui.showBank();
            }
        });
        
        elements.repayBtn.addEventListener('click', async () => {
            const amount = parseInt(elements.repayAmount.value);
            
            if (isNaN(amount) || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }
            
            const data = await api.bankAction(gameState.gameId, 'repay', amount);
            
            if (data) {
                game.loadGameState(data);
                ui.showBank();
            }
        });
        
        elements.backFromBankBtn.addEventListener('click', () => {
            ui.showMainMenu();
        });
        
        // Hospital
        elements.healBtn.addEventListener('click', async () => {
            const data = await api.hospitalAction(gameState.gameId);
            
            if (data) {
                game.loadGameState(data);
                ui.showMainMenu();
            }
        });
        
        elements.backFromHospitalBtn.addEventListener('click', () => {
            // Don't show available stocks when returning from hospital
            gameState.show_stocks = false;
            ui.showMainMenu();
        });
        
        // Broker
        // Add input validation to ensure integers for broker repay amount
        elements.brokerRepayAmount.addEventListener('input', () => {
            // Remove any non-digit characters
            elements.brokerRepayAmount.value = elements.brokerRepayAmount.value.replace(/\D/g, '');
            
            // Ensure it's not empty
            if (elements.brokerRepayAmount.value === '') {
                elements.brokerRepayAmount.value = '1';
            }
            
            // Ensure it's within min/max range
            const value = parseInt(elements.brokerRepayAmount.value);
            const max = parseInt(elements.brokerRepayAmount.max);
            if (value > max) {
                elements.brokerRepayAmount.value = max.toString();
            }
        });
        
        elements.brokerRepayBtn.addEventListener('click', async () => {
            const amount = parseInt(elements.brokerRepayAmount.value);
            
            if (isNaN(amount) || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }
            
            const data = await api.brokerAction(gameState.gameId, amount);
            
            if (data) {
                game.loadGameState(data);
                ui.showMainMenu();
            }
        });
        
        elements.backFromBrokerBtn.addEventListener('click', () => {
            // Don't show available stocks when returning from broker
            gameState.show_stocks = false;
            ui.showMainMenu();
        });
        
        // Trading App
        elements.upgradeBtn.addEventListener('click', async () => {
            const data = await api.tradingAppAction(gameState.gameId);
            
            if (data) {
                game.loadGameState(data);
                ui.showMainMenu();
            }
        });
        
        elements.backFromTradingAppBtn.addEventListener('click', () => {
            // Don't show available stocks when returning from trading app
            gameState.show_stocks = false;
            ui.showMainMenu();
        });
        
        // Darkweb
        elements.darkwebBtn.addEventListener('click', async () => {
            const data = await api.darkwebAction(gameState.gameId);
            
            if (data) {
                game.loadGameState(data);
                ui.showMainMenu();
            }
        });
        
        elements.backFromDarkwebBtn.addEventListener('click', () => {
            // Don't show available stocks when returning from darkweb
            gameState.show_stocks = false;
            ui.showMainMenu();
        });
        
        // High Scores
        elements.backFromHighScoresBtn.addEventListener('click', () => {
            // Don't show available stocks when returning from high scores
            gameState.show_stocks = false;
            ui.showMainMenu();
        });
        
        // Help
        elements.backFromHelpBtn.addEventListener('click', () => {
            // Don't show available stocks when returning from help
            gameState.show_stocks = false;
            ui.showMainMenu();
        });
        
        // Game Over
        elements.newGameBtn.addEventListener('click', () => {
            ui.showScreen('welcome-screen');
        });
        
        // Chart Screen
        elements.backFromChartBtn.addEventListener('click', () => {
            ui.showScreen('welcome-screen');
        });
    },
    
    // Load game state
    loadGameState: (data) => {
        gameState.gameId = data.game_id;
        gameState.token = data.token;  // Store the token in the gameState
        gameState.player = data.player;
        gameState.availableStocks = data.available_stocks;
        gameState.portfolio = data.portfolio;
        gameState.headline = data.headline;
        gameState.newsReports = data.news_reports;
        gameState.message = data.message;
        gameState.current_day = data.current_day;
        gameState.netWorthHistory = data.net_worth_history;
        gameState.showStocks = data.show_stocks;
        
        // Update UI
        ui.updatePlayerStatus();
        ui.showMessage(data.message);
        
        // Apply headline animation
        if (data.headline) {
            // Format headline with colored agency name
            const agency = data.headline.agency;
            const agencyClass = getAgencyColorClass(agency);
            const headlineText = `[<span class="${agencyClass}">${agency}</span>] ${data.headline.text}`;
            
            // Reset animation by cloning the element
            const oldHeadline = elements.headline;
            const newHeadline = oldHeadline.cloneNode(false);
            newHeadline.innerHTML = headlineText; // Use innerHTML to render the HTML
            oldHeadline.parentNode.replaceChild(newHeadline, oldHeadline);
            
            // Update the elements reference
            elements.headline = newHeadline;
        }
        
        // Check if game is over (days_left <= 0 or health <= 0)
        if (data.game_over || data.player.days_left <= 0 || data.player.health <= 0) {
            // If game is over, show game over screen with net worth chart
            ui.showGameOver(data);
            return; // Don't show news or stocks when game is over
        }
        
        // Only show news and stocks if game is not over
        if (gameState.newsReports && gameState.newsReports.length > 0 && !gameState.newsShown) {
            // Set the flag to indicate news has been shown
            gameState.newsShown = true;
            ui.showNewsReports();
        } else if (gameState.showStocks) {
            // Clear the flag to prevent showing stocks again
            gameState.showStocks = false;
            
            // Show available stocks
            ui.showAvailableStocks();
        }
    }
};

// Helper function to get color class for news agency
function getAgencyColorClass(agency) {
    switch (agency) {
        case 'CNN':
            return 'agency-cnn'; // Red
        case 'FOX':
            return 'agency-fox'; // Blue
        case 'CNBC':
            return 'agency-cnbc'; // Blue
        case 'WSJ':
            return 'agency-wsj'; // Black/Gray
        case 'BBC':
            return 'agency-bbc'; // Red
        case 'Bloomberg':
            return 'agency-bloomberg'; // Blue
        case 'Reuters':
            return 'agency-reuters'; // Orange
        case 'AP':
            return 'agency-ap'; // Black
        case 'NYT':
            return 'agency-nyt'; // Black
        default:
            return 'agency-default'; // Default color
    }
};

// Headline rotation
let headlineInterval = null;

// Function to update headline
const updateHeadline = async () => {
    // Use token if available, otherwise use gameId
    const idToUse = gameState.token || gameState.gameId;
    
    if (idToUse) {
        try {
            // Get fresh game state to update headline
            const data = await api.getGame(idToUse);
            if (data && data.headline) {
                gameState.headline = data.headline;
                
                // Format headline with colored agency name
                const agency = data.headline.agency;
                const agencyClass = getAgencyColorClass(agency);
                const headlineText = `[<span class="${agencyClass}">${agency}</span>] ${data.headline.text}`;
                
                // Reset animation by cloning the element
                const oldHeadline = elements.headline;
                const newHeadline = oldHeadline.cloneNode(false);
                newHeadline.innerHTML = headlineText; // Use innerHTML to render the HTML
                oldHeadline.parentNode.replaceChild(newHeadline, oldHeadline);
                
                // Update the elements reference
                elements.headline = newHeadline;
            }
        } catch (error) {
            console.error('Error updating headline:', error);
        }
    }
};

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    game.init();
    
    // Start headline rotation every 20 seconds
    headlineInterval = setInterval(updateHeadline, 20000);
});
