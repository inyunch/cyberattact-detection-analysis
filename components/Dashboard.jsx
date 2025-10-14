import React, { useState } from 'react';
import Sidebar from './Sidebar';
import TabSystem from './TabSystem';
import './Dashboard.css';

const Dashboard = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeMenuItem, setActiveMenuItem] = useState('dashboard');
  const [activeTab, setActiveTab] = useState('overview');

  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: '🏠',
    },
    {
      id: 'analytics',
      label: 'IDA/EDA Analysis',
      icon: '📊',
    },
    {
      id: 'threats',
      label: 'Global Threats',
      icon: '🌍',
    },
    {
      id: 'intrusion',
      label: 'Intrusion Detection',
      icon: '🛡️',
    },
    {
      id: 'insights',
      label: 'Comparative Insights',
      icon: '💡',
    },
    {
      id: 'methodology',
      label: 'Methodology',
      icon: '📚',
    },
  ];

  const tabs = [
    {
      id: 'overview',
      label: 'Overview',
      icon: '📈',
    },
    {
      id: 'threats',
      label: 'Threat Analysis',
      icon: '⚠️',
      badge: 5,
    },
    {
      id: 'network',
      label: 'Network Activity',
      icon: '🔗',
    },
    {
      id: 'alerts',
      label: 'Security Alerts',
      icon: '🚨',
      badge: 12,
    },
    {
      id: 'reports',
      label: 'Reports',
      icon: '📄',
    },
  ];

  return (
    <div className="dashboard-container">
      <Sidebar
        menuItems={menuItems}
        activeItem={activeMenuItem}
        onMenuClick={setActiveMenuItem}
        isCollapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      <main className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <header className="page-header">
          <div className="header-content">
            <h1 className="page-title">Cybersecurity Threat Analysis</h1>
            <p className="page-subtitle">Real-time monitoring and threat intelligence dashboard</p>
          </div>

          <div className="header-actions">
            <button className="header-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
            <button className="header-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span className="notification-badge">3</span>
            </button>
          </div>
        </header>

        <div className="tab-container">
          <TabSystem
            tabs={tabs}
            activeTab={activeTab}
            onTabChange={setActiveTab}
            variant="underline"
          />
        </div>

        <div className="content-area">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon success">✓</div>
              <div className="stat-content">
                <p className="stat-label">Active Connections</p>
                <h3 className="stat-value">1,284</h3>
                <p className="stat-change positive">↑ 12% from last hour</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon warning">⚠</div>
              <div className="stat-content">
                <p className="stat-label">Threats Detected</p>
                <h3 className="stat-value">47</h3>
                <p className="stat-change negative">↑ 8% from yesterday</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon info">🔍</div>
              <div className="stat-content">
                <p className="stat-label">Scanned Packets</p>
                <h3 className="stat-value">2.4M</h3>
                <p className="stat-change neutral">— No change</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon danger">🚨</div>
              <div className="stat-content">
                <p className="stat-label">Critical Alerts</p>
                <h3 className="stat-value">5</h3>
                <p className="stat-change positive">↓ 60% from last week</p>
              </div>
            </div>
          </div>

          <div className="chart-grid">
            <div className="chart-card">
              <h3 className="card-title">Threat Distribution</h3>
              <div className="chart-placeholder">
                <p>Your Plotly/Chart.js visualization goes here</p>
              </div>
            </div>

            <div className="chart-card">
              <h3 className="card-title">Network Activity</h3>
              <div className="chart-placeholder">
                <p>Your Plotly/Chart.js visualization goes here</p>
              </div>
            </div>
          </div>

          <div className="table-card">
            <div className="card-header">
              <h3 className="card-title">Recent Security Events</h3>
              <button className="card-action-btn">View All →</button>
            </div>
            <div className="table-placeholder">
              <p>Your data table component goes here</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
