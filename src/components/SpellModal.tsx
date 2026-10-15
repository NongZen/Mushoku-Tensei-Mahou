import React, { useEffect, useState } from 'react';
import { Spell } from '../types';
import { X, Volume2, Copy, Check, Dumbbell } from 'lucide-react';

interface SpellModalProps {
  spell: Spell | null;
  onClose: () => void;
  onPracticeSpell: (spell: Spell) => void;
}

export const SpellModal: React.FC<SpellModalProps> = ({ spell, onClose, onPracticeSpell }) => {
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    if (spell) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    } else {
      document.body.style.overflow = 'auto';
    }

    return () => {
      document.body.style.overflow = 'auto';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [spell, onClose]);

  if (!spell) return null;

  const copyToClipboard = async (text: string, key: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedKey(key);
      setTimeout(() => setCopiedKey(null), 2000);
    } catch {
      // fallback
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopiedKey(key);
      setTimeout(() => setCopiedKey(null), 2000);
    }
  };

  const playVoice = (text: string, lang: 'ja-JP' | 'th-TH' = 'ja-JP') => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported in this browser environment.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  const isSword = spell.element === 'Sword' || !!spell.sword_school;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/80 backdrop-blur-md" onClick={onClose} />

      {/* Modal Content */}
      <div className="modal-content relative w-full max-w-2xl rounded-2xl p-6 sm:p-8 text-left overflow-hidden z-10 max-h-[90vh] overflow-y-auto">
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white bg-white/5 hover:bg-white/10 rounded-full p-2 transition-colors focus:outline-none cursor-pointer"
          aria-label="Close modal"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="text-center mb-6 mt-2">
          <h3 className="font-cinzel text-3xl sm:text-4xl font-bold text-magic-gold mb-1 text-glow">
            {spell.en}
          </h3>
          <h4 className="text-lg text-magic-gold-light font-medium tracking-wide">
            {spell.romaji_name} ({spell.jp_name})
          </h4>
          <div className="text-sm text-gray-400 font-light mt-0.5">
            {spell.name.split('(')[0].trim()}
          </div>
          <div className="inline-block px-3 py-1 bg-magic-gold/10 border border-magic-gold/30 rounded-full text-magic-gold-light text-xs mt-3 shadow-[0_0_10px_rgba(197,160,89,0.2)]">
            <span>{spell.rank} • {spell.element_th || spell.element}</span>
            {spell.sword_school_th && <span className="ml-1.5 font-semibold text-yellow-300">• {spell.sword_school_th}</span>}
          </div>
        </div>

        <div className="space-y-4">
          {/* 1. Japanese Chant / Stance */}
          <div className="bg-black/40 rounded-xl p-5 border-l-4 border-blue-500/70 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
            <div className="flex justify-between items-center mb-2">
              <h5 className="text-xs uppercase tracking-wider text-blue-400 font-cinzel font-semibold flex items-center gap-1.5">
                <span>{isSword ? '🗡️' : '⛩️'}</span> 1. Japanese ({isSword ? 'คำสั่งกระบวนท่าภาษาญี่ปุ่น' : 'คำร่ายภาษาญี่ปุ่น'})
              </h5>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => playVoice(spell.jp)}
                  className="text-xs text-blue-400 hover:text-blue-300 font-cinzel flex items-center gap-1 cursor-pointer"
                >
                  <Volume2 className="w-3.5 h-3.5" /> Voice
                </button>
                <button
                  type="button"
                  onClick={() => copyToClipboard(spell.jp, 'jp')}
                  className="text-xs text-blue-400 hover:text-blue-300 font-cinzel flex items-center gap-1 cursor-pointer"
                >
                  {copiedKey === 'jp' ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                  {copiedKey === 'jp' ? 'Copied!' : 'Copy'}
                </button>
              </div>
            </div>
            <p className="font-jp text-base sm:text-lg text-gray-100 leading-relaxed font-bold">
              {spell.jp}
            </p>
          </div>

          {/* 2. Romaji */}
          <div className="bg-black/40 rounded-xl p-5 border-l-4 border-purple-500/70 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
            <div className="flex justify-between items-center mb-2">
              <h5 className="text-xs uppercase tracking-wider text-purple-400 font-cinzel font-semibold flex items-center gap-1.5">
                <span>🔤</span> 2. Romaji (คำอ่านโรมะจิ)
              </h5>
              <button
                type="button"
                onClick={() => copyToClipboard(spell.romaji, 'romaji')}
                className="text-xs text-purple-400 hover:text-purple-300 font-cinzel flex items-center gap-1 cursor-pointer"
              >
                {copiedKey === 'romaji' ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copiedKey === 'romaji' ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <p className="text-sm sm:text-base text-magic-gold-light leading-relaxed italic">
              {spell.romaji}
            </p>
          </div>

          {/* 3. Thai */}
          <div className="bg-black/40 rounded-xl p-5 border-l-4 border-magic-gold relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-r from-magic-gold/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
            <div className="flex justify-between items-center mb-2">
              <h5 className="text-xs uppercase tracking-wider text-magic-gold font-cinzel font-semibold flex items-center gap-1.5">
                <span>{isSword ? '⚔️' : '📖'}</span> 3. Thai ({isSword ? 'คำอธิบายกระบวนท่าภาษาไทย' : 'คำแปลภาษาไทย'})
              </h5>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => playVoice(spell.th, 'th-TH')}
                  className="text-xs text-magic-gold hover:text-yellow-300 font-cinzel flex items-center gap-1 cursor-pointer"
                >
                  <Volume2 className="w-3.5 h-3.5" /> TH Voice
                </button>
                <button
                  type="button"
                  onClick={() => copyToClipboard(spell.th, 'th')}
                  className="text-xs text-magic-gold hover:text-yellow-300 font-cinzel flex items-center gap-1 cursor-pointer"
                >
                  {copiedKey === 'th' ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                  {copiedKey === 'th' ? 'Copied!' : 'Copy'}
                </button>
              </div>
            </div>
            <p className="text-base sm:text-lg text-gray-200 leading-relaxed font-light italic whitespace-pre-line">
              "{spell.th}"
            </p>
          </div>

          {/* Spell / Technique Effect & Mechanics */}
          <div className="bg-black/30 rounded-xl p-4 border border-white/5 flex flex-col sm:flex-row justify-between gap-3 text-xs text-gray-400">
            <div>
              <strong className="text-gray-300">{isSword ? 'Stamina / MP:' : 'MP Cost:'}</strong>{' '}
              <span className="text-cyan-400 font-semibold">{spell.mp_cost} MP</span>
            </div>
            <div>
              <strong className="text-gray-300">Rank:</strong>{' '}
              <span className="text-yellow-400 font-semibold">{spell.rank}</span>
            </div>
            <div>
              <strong className="text-gray-300">{isSword ? 'Users:' : 'Casters:'}</strong>{' '}
              <span className="text-white font-medium">{spell.casters.join(', ')}</span>
            </div>
          </div>

          {spell.effect && (
            <div className="text-xs text-gray-400 bg-white/[0.03] p-3 rounded-lg border border-white/5">
              <strong className="text-magic-gold">Effect:</strong> {spell.effect}
            </div>
          )}

          {/* Practice Button (Only for magic spells; sword techniques do not have chants to practice) */}
          {!isSword && (
            <div className="text-center pt-2">
              <button
                type="button"
                onClick={() => {
                  onClose();
                  onPracticeSpell(spell);
                }}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-magic-gold to-yellow-500 text-magic-dark font-cinzel font-bold text-sm uppercase tracking-wider hover:scale-[1.02] transition-transform flex items-center justify-center gap-2 cursor-pointer shadow-[0_0_20px_rgba(197,160,89,0.3)]"
              >
                <Dumbbell className="w-4 h-4" />
                Practice This Spell In Training Mode
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
