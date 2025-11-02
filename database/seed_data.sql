-- Seed data for AirSense India database

-- Insert sample policies
INSERT INTO policies (policy_name, description, implementation_date, expected_reduction, actual_reduction, status, effectiveness_score, created_at) VALUES
('Odd-Even Vehicle Scheme', 'Alternate day vehicle restrictions based on registration numbers', '2024-01-15', 25.0, 23.0, 'active', 92.0, NOW()),
('BS-VI Emission Standards', 'Implementation of Bharat Stage VI emission standards for all new vehicles', '2023-04-01', 20.0, 18.0, 'active', 90.0, NOW()),
('Construction Activity Ban', 'Seasonal ban on construction activities during high pollution months', '2024-11-01', 15.0, 15.0, 'seasonal', 100.0, NOW()),
('Industrial Emission Control', 'Stricter emission norms for industries with real-time monitoring', '2023-07-01', 18.0, 14.0, 'active', 77.8, NOW()),
('Green Tax Implementation', 'Additional tax on older, polluting vehicles', '2024-03-01', 12.0, 12.0, 'active', 100.0, NOW()),
('Public Transport Enhancement', 'Expansion of metro and electric bus fleet', '2023-09-01', 22.0, 16.0, 'active', 72.7, NOW());

-- Insert sample community reports
INSERT INTO community_reports (user_id, location, pollution_type, description, lat, lng, verified, votes, created_at) VALUES
('user_001', 'Connaught Place, Delhi', 'Construction Dust', 'Heavy construction dust from metro expansion work causing visibility issues', 28.6315, 77.2167, true, 45, NOW() - INTERVAL '2 days'),
('user_002', 'Andheri West, Mumbai', 'Industrial Smoke', 'Thick black smoke from nearby industrial unit during evening hours', 19.1136, 72.8697, true, 32, NOW() - INTERVAL '1 day'),
('user_003', 'Koramangala, Bangalore', 'Garbage Burning', 'Open garbage burning reported near residential area', 12.9352, 77.6245, false, 18, NOW() - INTERVAL '5 hours'),
('user_004', 'Salt Lake, Kolkata', 'Vehicular Emissions', 'Heavy traffic congestion causing severe pollution during peak hours', 22.5744, 88.4120, true, 28, NOW() - INTERVAL '3 days'),
('user_005', 'T Nagar, Chennai', 'Construction Dust', 'Multiple construction sites without proper dust control measures', 13.0418, 80.2341, true, 21, NOW() - INTERVAL '1 day'),
('user_006', 'Hitech City, Hyderabad', 'Vehicular Emissions', 'Road widening work causing major traffic and pollution issues', 17.4485, 78.3908, false, 15, NOW() - INTERVAL '6 hours');

-- Insert sample user activities
INSERT INTO user_activity (user_id, action_type, points_earned, created_at) VALUES
('user_001', 'report_submitted', 50, NOW() - INTERVAL '2 days'),
('user_001', 'report_verified', 100, NOW() - INTERVAL '1 day'),
('user_001', 'milestone_reached', 200, NOW() - INTERVAL '12 hours'),
('user_002', 'report_submitted', 50, NOW() - INTERVAL '1 day'),
('user_002', 'report_verified', 100, NOW() - INTERVAL '6 hours'),
('user_003', 'report_submitted', 50, NOW() - INTERVAL '5 hours'),
('user_004', 'report_submitted', 50, NOW() - INTERVAL '3 days'),
('user_004', 'report_verified', 100, NOW() - INTERVAL '2 days'),
('user_005', 'report_submitted', 50, NOW() - INTERVAL '1 day'),
('user_005', 'report_verified', 100, NOW() - INTERVAL '12 hours');

-- Insert sample historical AQI readings for Delhi
INSERT INTO aqi_readings (city, aqi, pm25, pm10, no2, so2, co, o3, lat, lng, timestamp) VALUES
('Delhi', 287, 167, 245, 68, 22, 2.8, 42, 28.7041, 77.1025, NOW() - INTERVAL '1 day'),
('Delhi', 312, 189, 278, 74, 26, 3.2, 48, 28.7041, 77.1025, NOW() - INTERVAL '2 days'),
('Delhi', 265, 152, 223, 62, 19, 2.5, 38, 28.7041, 77.1025, NOW() - INTERVAL '3 days'),
('Delhi', 298, 175, 256, 71, 24, 3.0, 45, 28.7041, 77.1025, NOW() - INTERVAL '4 days'),
('Delhi', 245, 142, 208, 58, 18, 2.3, 35, 28.7041, 77.1025, NOW() - INTERVAL '5 days');

-- Insert sample AQI readings for other cities
INSERT INTO aqi_readings (city, aqi, pm25, pm10, no2, so2, co, o3, lat, lng, timestamp) VALUES
('Mumbai', 178, 98, 142, 45, 14, 1.8, 28, 19.0760, 72.8777, NOW() - INTERVAL '1 day'),
('Bangalore', 142, 78, 115, 38, 11, 1.4, 22, 12.9716, 77.5946, NOW() - INTERVAL '1 day'),
('Kolkata', 198, 112, 165, 52, 16, 2.1, 32, 22.5726, 88.3639, NOW() - INTERVAL '1 day'),
('Chennai', 135, 72, 108, 35, 10, 1.3, 20, 13.0827, 80.2707, NOW() - INTERVAL '1 day'),
('Hyderabad', 156, 88, 128, 42, 13, 1.6, 25, 17.3850, 78.4867, NOW() - INTERVAL '1 day'),
('Pune', 148, 82, 121, 40, 12, 1.5, 24, 18.5204, 73.8567, NOW() - INTERVAL '1 day'),
('Ahmedabad', 167, 94, 138, 46, 14, 1.7, 27, 23.0225, 72.5714, NOW() - INTERVAL '1 day'),
('Jaipur', 212, 122, 178, 56, 17, 2.2, 34, 26.9124, 75.7873, NOW() - INTERVAL '1 day'),
('Lucknow', 228, 132, 192, 61, 19, 2.4, 37, 26.8467, 80.9462, NOW() - INTERVAL '1 day');

-- Insert sample predictions
INSERT INTO predictions (city, prediction_time, predicted_aqi, confidence, model_version, created_at) VALUES
('Delhi', NOW() + INTERVAL '1 hour', 295, 94.5, 'v2.0-lstm', NOW()),
('Delhi', NOW() + INTERVAL '2 hours', 302, 94.0, 'v2.0-lstm', NOW()),
('Delhi', NOW() + INTERVAL '3 hours', 288, 93.5, 'v2.0-lstm', NOW()),
('Mumbai', NOW() + INTERVAL '1 hour', 182, 94.2, 'v2.0-lstm', NOW()),
('Bangalore', NOW() + INTERVAL '1 hour', 145, 94.8, 'v2.0-lstm', NOW());

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_aqi_city_timestamp ON aqi_readings(city, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_reports_verified ON community_reports(verified, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reports_location ON community_reports(lat, lng);
CREATE INDEX IF NOT EXISTS idx_user_activity_user ON user_activity(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_city ON predictions(city, prediction_time);
CREATE INDEX IF NOT EXISTS idx_policies_status ON policies(status, implementation_date);

-- Create views for common queries
CREATE OR REPLACE VIEW recent_aqi_readings AS
SELECT 
    city,
    aqi,
    pm25,
    pm10,
    timestamp,
    CASE 
        WHEN aqi <= 50 THEN 'Good'
        WHEN aqi <= 100 THEN 'Moderate'
        WHEN aqi <= 200 THEN 'Poor'
        WHEN aqi <= 300 THEN 'Very Poor'
        ELSE 'Severe'
    END as category
FROM aqi_readings
WHERE timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;

CREATE OR REPLACE VIEW verified_community_reports AS
SELECT 
    id,
    location,
    pollution_type,
    description,
    lat,
    lng,
    votes,
    created_at
FROM community_reports
WHERE verified = true
ORDER BY votes DESC, created_at DESC;

CREATE OR REPLACE VIEW policy_effectiveness_summary AS
SELECT 
    policy_name,
    status,
    expected_reduction,
    actual_reduction,
    effectiveness_score,
    ROUND((actual_reduction / expected_reduction * 100)::numeric, 2) as achievement_percentage,
    implementation_date
FROM policies
WHERE status = 'active'
ORDER BY effectiveness_score DESC;

-- Insert sample alert settings
CREATE TABLE IF NOT EXISTS alert_settings (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    aqi_threshold FLOAT DEFAULT 200,
    notification_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, city)
);

INSERT INTO alert_settings (user_id, city, aqi_threshold, notification_enabled) VALUES
('user_001', 'Delhi', 200, true),
('user_002', 'Mumbai', 150, true),
('user_003', 'Bangalore', 180, true),
('user_004', 'Kolkata', 200, true),
('user_005', 'Chennai', 150, true);

-- Grant permissions (adjust based on your database user)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO airsense_app;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO airsense_app;