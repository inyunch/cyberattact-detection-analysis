import React, { useState, useRef, useEffect } from 'react';
import './TabSystem.css';

const TabSystem = ({ tabs, activeTab, onTabChange, variant = 'underline' }) => {
  const [indicatorStyle, setIndicatorStyle] = useState({});
  const tabRefs = useRef({});

  useEffect(() => {
    const activeTabElement = tabRefs.current[activeTab];
    if (activeTabElement) {
      const { offsetLeft, offsetWidth } = activeTabElement;
      setIndicatorStyle({
        left: `${offsetLeft}px`,
        width: `${offsetWidth}px`,
      });
    }
  }, [activeTab]);

  return (
    <div className={`tab-system tab-system--${variant}`}>
      <div className="tab-list" role="tablist">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            ref={(el) => (tabRefs.current[tab.id] = el)}
            className={`tab ${activeTab === tab.id ? 'active' : ''} ${tab.disabled ? 'disabled' : ''}`}
            onClick={() => !tab.disabled && onTabChange(tab.id)}
            role="tab"
            aria-selected={activeTab === tab.id}
            aria-controls={`tabpanel-${tab.id}`}
            disabled={tab.disabled}
          >
            {tab.icon && <span className="tab-icon">{tab.icon}</span>}
            <span className="tab-label">{tab.label}</span>
            {tab.badge && (
              <span className="tab-badge" aria-label={`${tab.badge} notifications`}>
                {tab.badge}
              </span>
            )}
          </button>
        ))}
        {variant === 'underline' && (
          <div className="tab-indicator" style={indicatorStyle} />
        )}
      </div>
    </div>
  );
};

export default TabSystem;
