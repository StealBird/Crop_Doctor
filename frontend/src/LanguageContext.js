// ============================================================
// LanguageContext.js  —  Crop Doctor Language System
// Provides: LanguageProvider, useLanguage
//
// HOW TO USE IN ANY COMPONENT:
//   import { useLanguage } from '../LanguageContext';
//   const { t, lang, switchLang, langCode } = useLanguage();
//   <button>{t('diagnose_button')}</button>
//   <button>{t('chat_healthy', { crop: 'Tomato' })}</button>
//
// Language codes stored: 'EN' | 'HI' | 'MR' | 'HL'
// langCode maps to API string: 'english' | 'hindi' | 'marathi' | 'hinglish'
// ============================================================

import { createContext, useContext, useState, useCallback } from 'react';
import translations from './translations';

const LanguageContext = createContext(null);

export const LANG_OPTIONS = [
  { code: 'EN', label: 'English',  flag: '🇬🇧' },
  { code: 'HI', label: 'हिंदी',    flag: '🇮🇳' },
  { code: 'MR', label: 'मराठी',    flag: '🌿' },
  { code: 'HL', label: 'Hinglish', flag: '🤝' },
];

const LANG_API_MAP = {
  EN: 'english',
  HI: 'hindi',
  MR: 'marathi',
  HL: 'hinglish',
};

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(
    () => localStorage.getItem('crop_doctor_lang') || 'EN'
  );

  const switchLang = useCallback((code) => {
    setLang(code);
    localStorage.setItem('crop_doctor_lang', code);
  }, []);

  // t('key') — returns translated string for current language
  // t('key', { crop: 'Tomato' }) — replaces {crop} placeholder
  const t = useCallback(
    (key, vars = {}) => {
      let text =
        translations[lang]?.[key] ||
        translations['EN']?.[key] ||
        key;
      Object.entries(vars).forEach(([k, v]) => {
        text = text.replace(`{${k}}`, v ?? '');
      });
      return text;
    },
    [lang]
  );

  // API language string expected by /chat and /predict backends
  const langCode = LANG_API_MAP[lang] || 'english';

  return (
    <LanguageContext.Provider value={{ lang, switchLang, t, langCode }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useLanguage must be used inside <LanguageProvider>');
  return ctx;
}

// ── Backward-compat shim ────────────────────────────────────
// Components that still call useTranslation() keep working.
export function useTranslation() {
  const { t } = useLanguage();
  return t;
}

// ── Legacy LANGUAGE_TO_API shim ─────────────────────────────
export const LANGUAGE_TO_API = LANG_API_MAP;
