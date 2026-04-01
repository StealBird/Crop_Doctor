// ============================================================
// LanguageContext.js  —  Crop Doctor Language System
// Provides: LanguageProvider, useLanguage, useTranslation
//
// HOW TO USE IN ANY COMPONENT:
//   import { useTranslation } from '../LanguageContext';
//   const t = useTranslation();
//   <button>{t('diagnose_button')}</button>
// ============================================================

import React, { createContext, useContext, useState } from 'react';
import translations from './translations';

// Supported languages — order matters (shown in dropdown)
export const LANGUAGES = [
  { code: 'english',  label: 'English' },
  { code: 'hindi',    label: 'हिंदी' },
  { code: 'marathi',  label: 'मराठी' },
  { code: 'hinglish', label: 'Hinglish' },
];

// Map language code → API language string expected by your /chat backend
export const LANGUAGE_TO_API = {
  english:  'english',
  hindi:    'hindi',
  marathi:  'marathi',
  hinglish: 'hinglish',
};

// ── Context ────────────────────────────────────────────────
const LanguageContext = createContext(null);

// ── Provider  ──────────────────────────────────────────────
// Wrap your entire app with this in index.js or App.js:
//   <LanguageProvider>
//     <App />
//   </LanguageProvider>

export function LanguageProvider({ children }) {
  // Read saved language from localStorage, default to 'english'
  const [language, setLanguage] = useState(
    () => localStorage.getItem('cropDoctorLanguage') || 'english'
  );

  const changeLanguage = (newLang) => {
    setLanguage(newLang);
    localStorage.setItem('cropDoctorLanguage', newLang);
  };

  return (
    <LanguageContext.Provider value={{ language, changeLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

// ── Hook: useLanguage ───────────────────────────────────────
// Returns { language, changeLanguage }
// Use when you need to read or change the current language code.
export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useLanguage must be used inside <LanguageProvider>');
  return ctx;
}

// ── Hook: useTranslation ────────────────────────────────────
// Returns t(key) function.
// t('diagnose_button')  →  "Diagnose Now" / "निदान करें" / etc.
// t('unknown_key')      →  'unknown_key'  (safe fallback)
export function useTranslation() {
  const { language } = useLanguage();

  const t = (key) => {
    const langStrings = translations[language] || translations['english'];
    return langStrings[key] ?? translations['english'][key] ?? key;
  };

  return t;
}

// ── LanguageSelector Component ──────────────────────────────
// Drop-in selector for the top-right of your header.
// Usage: <LanguageSelector />

export function LanguageSelector() {
  const { language, changeLanguage } = useLanguage();
  const t = useTranslation();

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-400 hidden sm:inline">
        {t('language_label')}
      </span>
      <select
        value={language}
        onChange={(e) => changeLanguage(e.target.value)}
        className="
          bg-gray-800 text-white text-sm
          border border-gray-600 rounded-lg
          px-3 py-1.5 cursor-pointer
          hover:border-green-500 focus:border-green-500
          focus:outline-none transition-colors
        "
        aria-label={t('language_label')}
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.label}
          </option>
        ))}
      </select>
    </div>
  );
}
