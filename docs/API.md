# Stock Trading Simulator API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
The API uses session-based authentication. All trading endpoints require authentication.

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string" // optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "username": "string",
    "user_id": "number"
  }
}
```

#### Login User
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "string"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "user_id": "number",
    "username": "string",
    "email": "string",
    "balance": "number",
    "created_at": "string",
    "updated_at": "string"
  }
}
```

#### Logout User
```http
POST /auth/logout
```

#### Get Current User
```http
GET /auth/me
```

### Trading

#### Get Portfolio
```http
GET /trading/portfolio
```

**Response:**
```json
{
  "success": true,
  "portfolio": {
    "user_id": "number",
    "username": "string",
    "balance": "number",
    "portfolio_value": "number",
    "total_value": "number",
    "total_gain_loss": "number",
    "total_gain_loss_percent": "number",
    "portfolio": [
      {
        "symbol": "string",
        "shares": "number",
        "avg_price": "number",
        "current_price": "number",
        "market_value": "number",
        "gain_loss": "number",
        "gain_loss_percent": "number"
      }
    ]
  }
}
```

#### Buy Stock
```http
POST /trading/buy
```

**Request Body:**
```json
{
  "symbol": "string",
  "shares": "number"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully bought 10 shares of AAPL",
  "symbol": "AAPL",
  "shares": 10,
  "price": 150.25,
  "total_cost": 1502.50,
  "new_balance": 98497.50
}
```

#### Sell Stock
```http
POST /trading/sell
```

**Request Body:**
```json
{
  "symbol": "string",
  "shares": "number"
}
```

#### Get Transaction History
```http
GET /trading/transactions?limit=50
```

**Response:**
```json
{
  "success": true,
  "transactions": [
    {
      "symbol": "AAPL",
      "type": "BUY",
      "shares": 10,
      "price": 150.25,
      "total_amount": 1502.50,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get Watchlist
```http
GET /trading/watchlist
```

#### Add to Watchlist
```http
POST /trading/watchlist
```

**Request Body:**
```json
{
  "symbol": "string"
}
```

#### Remove from Watchlist
```http
DELETE /trading/watchlist/{symbol}
```

### Stocks

#### Search Stocks
```http
GET /stocks/search?q=AAPL
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "price": 150.25,
      "change": 2.50,
      "changePercent": 1.69,
      "volume": 50000000,
      "marketCap": 2500000000000,
      "sector": "Technology",
      "industry": "Consumer Electronics"
    }
  ]
}
```

#### Get Stock Info
```http
GET /stocks/info/{symbol}
```

#### Get Stock Price
```http
GET /stocks/price/{symbol}
```

**Response:**
```json
{
  "success": true,
  "symbol": "AAPL",
  "price": 150.25
}
```

#### Get Historical Data
```http
GET /stocks/historical/{symbol}?period=1mo
```

**Valid periods:** 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

**Response:**
```json
{
  "success": true,
  "symbol": "AAPL",
  "data": [
    {
      "date": "2024-01-15",
      "open": 148.50,
      "high": 152.00,
      "low": 147.25,
      "close": 150.25,
      "volume": 45000000
    }
  ]
}
```

#### Get Market Movers
```http
GET /stocks/movers
```

#### Validate Symbol
```http
GET /stocks/validate/{symbol}
```

#### Get Batch Prices
```http
POST /stocks/batch-prices
```

**Request Body:**
```json
{
  "symbols": ["AAPL", "GOOGL", "MSFT"]
}
```

## WebSocket Events

### Connection
```javascript
const socket = io('http://localhost:5000');
```

### Subscribe to Stock Updates
```javascript
socket.emit('subscribe_stock', { symbol: 'AAPL' });
```

### Unsubscribe from Stock Updates
```javascript
socket.emit('unsubscribe_stock', { symbol: 'AAPL' });
```

### Receive Price Updates
```javascript
socket.on('price_update', (data) => {
  console.log(data);
  // {
  //   symbol: 'AAPL',
  //   price: 150.25,
  //   timestamp: 1642248600
  // }
});
```

## Error Responses

All endpoints return errors in the following format:

```json
{
  "success": false,
  "message": "Error description"
}
```

Common HTTP status codes:
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (authentication required)
- `404` - Not Found (resource not found)
- `409` - Conflict (username already exists)
- `500` - Internal Server Error

## Rate Limits

The API uses free tier services and may have rate limits:
- Yahoo Finance: No official limits but recommended to not exceed 2000 requests/hour
- Stock price updates via WebSocket: Every 5 seconds per subscribed symbol

## Data Sources

- **Stock Data**: Yahoo Finance (yfinance library)
- **Real-time Updates**: WebSocket with 5-second intervals
- **Historical Data**: Yahoo Finance historical data API