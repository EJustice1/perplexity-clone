import React, { useState } from 'react';
import { toast } from 'react-hot-toast';

/**
 * Settings page component with user preferences and account settings
 * All functionality shows "not implemented yet" messages
 */
export default function Settings() {
  const [settings, setSettings] = useState({
    notifications: true,
    darkMode: false,
    language: 'en',
    autoSave: true,
    searchHistory: true,
    analytics: false
  });

  const handleSettingChange = (key: keyof typeof settings, value: string | boolean) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    toast('This setting will be saved in the next phase!', {
      duration: 2000,
      position: 'bottom-right',
      style: {
        background: '#363636',
        color: '#fff',
      },
    });
  };

  const handleSaveSettings = () => {
    toast('Settings will be saved to the backend in the next phase!', {
      duration: 3000,
      position: 'bottom-right',
      style: {
        background: '#363636',
        color: '#fff',
      },
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-gray-600">Manage your account preferences and settings</p>
      </div>

      <div className="space-y-8">
        {/* Account Settings */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Account Settings</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Email</label>
                <p className="text-sm text-gray-500">user@example.com</p>
              </div>
              <button
                onClick={() => toast('Email change functionality will be implemented in the next phase!')}
                className="px-4 py-2 text-sm text-blue-600 hover:text-blue-700 font-medium rounded-lg hover:bg-blue-50 transition-colors duration-200"
              >
                Change
              </button>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Password</label>
                <p className="text-sm text-gray-500">Last changed 30 days ago</p>
              </div>
              <button
                onClick={() => toast('Password change functionality will be implemented in the next phase!')}
                className="px-4 py-2 text-sm text-blue-600 hover:text-blue-700 font-medium rounded-lg hover:bg-blue-50 transition-colors duration-200"
              >
                Change
              </button>
            </div>
          </div>
        </div>

        {/* Preferences */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Preferences</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Notifications</label>
                <p className="text-sm text-gray-500">Receive email notifications</p>
              </div>
              <button
                onClick={() => handleSettingChange('notifications', !settings.notifications)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 ${
                  settings.notifications ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${
                  settings.notifications ? 'translate-x-6' : 'translate-x-1'
                }`} />
              </button>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Dark Mode</label>
                <p className="text-sm text-gray-500">Use dark theme</p>
              </div>
              <button
                onClick={() => handleSettingChange('darkMode', !settings.darkMode)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 ${
                  settings.darkMode ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${
                  settings.darkMode ? 'translate-x-6' : 'translate-x-1'
                }`} />
              </button>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Language</label>
                <p className="text-sm text-gray-500">Interface language</p>
              </div>
              <select
                value={settings.language}
                onChange={(e) => handleSettingChange('language', e.target.value)}
                className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </select>
            </div>
          </div>
        </div>

        {/* Search Settings */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Search Settings</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Auto-save searches</label>
                <p className="text-sm text-gray-500">Automatically save search history</p>
              </div>
              <button
                onClick={() => handleSettingChange('autoSave', !settings.autoSave)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 ${
                  settings.autoSave ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${
                  settings.autoSave ? 'translate-x-6' : 'translate-x-1'
                }`} />
              </button>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Search history</label>
                <p className="text-sm text-gray-500">Store search queries</p>
              </div>
              <button
                onClick={() => handleSettingChange('searchHistory', !settings.searchHistory)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 ${
                  settings.searchHistory ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${
                  settings.searchHistory ? 'translate-x-6' : 'translate-x-1'
                }`} />
              </button>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            onClick={handleSaveSettings}
            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}
