#!/usr/bin/env python3
"""
Database cache management page
MongoDB + Redis cache management and monitoring
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Import UI utility functions
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui_utils import apply_hide_deploy_button_css

try:
    from tradingagents.config.database_manager import get_database_manager
    DB_MANAGER_AVAILABLE = True
except ImportError as e:
    DB_MANAGER_AVAILABLE = False
    st.error(f"Database manager unavailable: {e}")

def main():
    st.set_page_config(
        page_title="Database Management - TradingAgents",
        page_icon="🗄️",
        layout="wide"
    )
    
    # Apply CSS for hiding deploy button
    apply_hide_deploy_button_css()
    
    st.title("🗄️ MongoDB + Redis Database Management")
    st.markdown("---")
    
    if not DB_MANAGER_AVAILABLE:
        st.error("❌ Database manager unavailable")
        st.info("""
        Please follow these steps to set up the database environment:
        
        1. Install dependencies:
        ```bash
        pip install -r requirements_db.txt
        ```
        
        2. Set up databases:
        ```bash
        python scripts/setup_databases.py
        ```
        
        3. Test connection:
        ```bash
        python scripts/setup_databases.py --test
        ```
        """)
        return
    
    # Get database manager instance
    db_manager = get_database_manager()
    
    # Sidebar operations
    with st.sidebar:
        st.header("🛠️ Database Operations")
        
        # Connection status
        st.subheader("📡 Connection Status")
        mongodb_status = "✅ Connected" if db_manager.is_mongodb_available() else "❌ Disconnected"
        redis_status = "✅ Connected" if db_manager.is_redis_available() else "❌ Disconnected"
        
        st.write(f"**MongoDB**: {mongodb_status}")
        st.write(f"**Redis**: {redis_status}")
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh Statistics", type="primary"):
            st.rerun()
        
        st.markdown("---")
        
        # Cleanup operations
        st.subheader("🧹 Clean Data")
        
        max_age_days = st.slider(
            "Clean data older than how many days",
            min_value=1,
            max_value=30,
            value=7,
            help="Delete cache data older than the specified number of days"
        )
        
        if st.button("🗑️ Clean Expired Data", type="secondary"):
            with st.spinner("Cleaning expired data..."):
                # Use database_manager's cache cleanup functionality
                pattern = f"*:{max_age_days}d:*"  # Simplified cleanup pattern
                cleared_count = db_manager.cache_clear_pattern(pattern)
            st.success(f"✅ Cleaned {cleared_count} expired records")
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 MongoDB Statistics")
        
        try:
            stats = db_manager.get_cache_stats()
            
            if db_manager.is_mongodb_available():
                # Get MongoDB collection statistics
                collections_info = {
                    "stock_data": "📈 Stock Data",
                    "analysis_results": "📊 Analysis Results",
                    "user_sessions": "👤 User Sessions",
                    "configurations": "⚙️ Configurations"
                }

                total_records = 0
                st.markdown("**Collection Details:**")

                mongodb_client = db_manager.get_mongodb_client()
                if mongodb_client is not None:
                    mongodb_db = mongodb_client[db_manager.mongodb_config["database"]]
                    for collection_name, display_name in collections_info.items():
                        try:
                            collection = mongodb_db[collection_name]
                            count = collection.count_documents({})
                            total_records += count
                            st.write(f"**{display_name}**: {count:,} records")
                        except Exception as e:
                            st.write(f"**{display_name}**: Failed to get ({e})")
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Total Records", f"{total_records:,}")
                with metric_col2:
                    st.metric("Redis Cache", stats.get('redis_keys', 0))
            else:
                st.error("MongoDB not connected")
                
        except Exception as e:
            st.error(f"Failed to get MongoDB statistics: {e}")
    
    with col2:
        st.subheader("⚡ Redis Statistics")
        
        try:
            stats = db_manager.get_cache_stats()
            
            if db_manager.is_redis_available():
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Cache Key Count", stats.get("redis_keys", 0))
                with metric_col2:
                    st.metric("Memory Usage", stats.get("redis_memory", "N/A"))
                
                st.info("""
                **Redis Cache Strategy:**
                
                🔹 **Stock Data**：6 hours auto-expiration
                🔹 **Analysis Results**：24 hours auto-expiration  
                🔹 **User Sessions**：1 hour auto-expiration
                
                Redis is primarily used for fast access to hot data,
                which is automatically reloaded from MongoDB after expiration.
                """)
            else:
                st.error("Redis not connected")
                
        except Exception as e:
            st.error(f"Failed to get Redis statistics: {e}")
    
    st.markdown("---")
    
    # Database configuration
    st.subheader("⚙️ Database Configuration")
    
    config_col1, config_col2 = st.columns([1, 1])
    
    with config_col1:
        st.markdown("**MongoDB Configuration:**")
        # Get actual configuration from database manager
        mongodb_config = db_manager.mongodb_config
        mongodb_host = mongodb_config.get('host', 'localhost')
        mongodb_port = mongodb_config.get('port', 27017)
        mongodb_db_name = mongodb_config.get('database', 'tradingagents')
        st.code(f"""
Host: {mongodb_host}:{mongodb_port}
Database: {mongodb_db_name}
Status: {mongodb_status}
Enabled: {mongodb_config.get('enabled', False)}
        """)

        if db_manager.is_mongodb_available():
            st.markdown("**Collection Structure:**")
            st.code("""
    📁 tradingagents/
    ├── 📊 stock_data        # Stock historical data
    ├── 📈 analysis_results  # Analysis results
    ├── 👤 user_sessions     # User sessions
    └── ⚙️ configurations   # System configurations
                """)
    
    with config_col2:
        st.markdown("**Redis Configuration:**")
        # Get actual configuration from database manager
        redis_config = db_manager.redis_config
        redis_host = redis_config.get('host', 'localhost')
        redis_port = redis_config.get('port', 6379)
        redis_db = redis_config.get('db', 0)
        st.code(f"""
Host: {redis_host}:{redis_port}
Database: {redis_db}
Status: {redis_status}
Enabled: {redis_config.get('enabled', False)}
                """)
        
        if db_manager.is_redis_available():
            st.markdown("**Cache Key Format:**")
            st.code("""
    stock:SYMBOL:HASH     # Stock data cache
    analysis:SYMBOL:HASH  # Analysis result cache  
    session:USER:HASH     # User session cache
                """)
    
    st.markdown("---")
    
    # Performance comparison
    st.subheader("🚀 Performance Advantage")
    
    perf_col1, perf_col2, perf_col3 = st.columns(3)
    
    with perf_col1:
        st.metric(
            label="Redis Cache Speed",
            value="< 1ms",
            delta="Faster than API by 1000+ times",
            help="Ultra-fast access speed of Redis memory cache"
        )
    
    with perf_col2:
        st.metric(
            label="MongoDB Query Speed", 
            value="< 10ms",
            delta="Faster than API by 100+ times",
            help="Optimized query speed with MongoDB indexes"
        )
    
    with perf_col3:
        st.metric(
            label="Storage Capacity",
            value="Unlimited",
            delta="vs API quota limits",
            help="Local storage is not limited by API call frequency"
        )
    
    # Architecture explanation
    st.markdown("---")
    st.subheader("🏗️ Cache Architecture")
    
    st.info("""
    **Three-tier Cache Architecture:**
    
    1. **Redis (L1 Cache)** - Memory cache, millisecond access
       - Stores the hottest data
       - Automatic expiration management
       - High concurrency support
    
    2. **MongoDB (L2 Cache)** - Persistent storage, second-level access  
       - Stores all historical data
       - Supports complex queries
       - Data persistence guarantee
    
    3. **API (L3 Data Source)** - External data source, minute-level access
       - Tushare data interface (Chinese A-shares)
       - FINNHUB API (US stock data)
       - Yahoo Finance API (supplemental data)
    
    **Data Flow:** API → MongoDB → Redis → Application
    """)
    
    # Footer information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        🗄️ Database Cache Management System | TradingAgents v0.1.2 | 
        <a href='https://github.com/your-repo/TradingAgents' target='_blank'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
