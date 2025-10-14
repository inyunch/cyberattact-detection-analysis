import React, { useState } from 'react';
import './Sidebar.css';

const Sidebar = ({ menuItems, activeItem, onMenuClick, isCollapsed, onToggle }) => {
  return (
    <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <div className="logo-container">
          <span className="logo-icon">🛡️</span>
          {!isCollapsed && (
            <div className="logo-text">
              <h1>CyberGuard</h1>
              <p>Threat Intelligence</p>
            </div>
          )}
        </div>
        <button
          className="toggle-btn"
          onClick={onToggle}
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            {isCollapsed ? (
              <path d="M9 18l6-6-6-6" />
            ) : (
              <path d="M15 18l-6-6 6-6" />
            )}
          </svg>
        </button>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activeItem === item.id ? 'active' : ''}`}
            onClick={() => onMenuClick(item.id)}
            aria-current={activeItem === item.id ? 'page' : undefined}
            title={isCollapsed ? item.label : ''}
          >
            <span className="nav-icon" aria-hidden="true">
              {item.icon}
            </span>
            {!isCollapsed && (
              <span className="nav-label">{item.label}</span>
            )}
            {activeItem === item.id && <span className="active-indicator" />}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        {!isCollapsed && (
          <div className="user-info">
            <div className="user-avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
              </svg>
            </div>
            <div className="user-details">
              <p className="user-name">Admin</p>
              <p className="user-role">Security Analyst</p>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
