export const BALLOON_COLORS = Object.freeze(['pink', 'red', 'pearl']);
export const COLOR_PREFERENCE_KEY = 'peyce-balloon-color-v1';

// This browser preference contains one visual enum, never session or answer data.
export function createColorPreference(storage = () => globalThis.localStorage) {
  return {
    read() {
      try { const value = storage()?.getItem(COLOR_PREFERENCE_KEY); return BALLOON_COLORS.includes(value) ? value : null; }
      catch { return null; }
    },
    save(value) {
      if (!BALLOON_COLORS.includes(value)) return false;
      try { const target = storage(); if (!target) return false; target.setItem(COLOR_PREFERENCE_KEY, value); return true; }
      catch { return false; }
    },
    clear() {
      try { storage()?.removeItem(COLOR_PREFERENCE_KEY); return true; }
      catch { return false; }
    },
  };
}
