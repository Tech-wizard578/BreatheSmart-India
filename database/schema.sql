-- AQI Readings Table
CREATE TABLE aqi_readings (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    aqi FLOAT NOT NULL,
    pm25 FLOAT,
    pm10 FLOAT,
    no2 FLOAT,
    so2 FLOAT,
    co FLOAT,
    o3 FLOAT,
    lat FLOAT,
    lng FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city_timestamp (city, timestamp)
);

-- Community Reports Table
CREATE TABLE community_reports (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    pollution_type VARCHAR(50),
    description TEXT,
    image_url VARCHAR(500),
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    votes INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_location (lat, lng)
);

-- Policies Table
CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    policy_name VARCHAR(200) NOT NULL,
    description TEXT,
    implementation_date DATE NOT NULL,
    expected_reduction FLOAT,
    actual_reduction FLOAT,
    status VARCHAR(50) DEFAULT 'active',
    effectiveness_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Activity Table
CREATE TABLE user_activity (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    action_type VARCHAR(50),
    points_earned INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id)
);

-- Predictions Table
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    prediction_time TIMESTAMP NOT NULL,
    predicted_aqi FLOAT NOT NULL,
    actual_aqi FLOAT,
    confidence FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);