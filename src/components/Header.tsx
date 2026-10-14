import React from 'react';
import { TabType } from '../types';
import { BookMarked, Mic, ShieldAlert } from 'lucide-react';

interface HeaderProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, onTabChange }) => {
  return (
    <header className="text-center mb-10">
      <div className="inline-block relative mb-4 group">
        <div className="absolute -inset-1.5 bg-gradient-to-r from-magic-gold via-yellow-300 to-magic-gold rounded-full blur-md opacity-40 group-hover:opacity-75 transition duration-500"></div>
        <img
          src="/icon.png"
          alt="Mushoku Tensei Emblem"
          onError={(e) => {
            // fallback if icon.png fails to load
            (e.target as HTMLElement).style.display = 'none';
          }}
          className="relative w-28 h-28 md:w-32 md:h-32 mx-auto rounded-full border-2 border-magic-gold shadow-[0_0_20px_rgba(197,160,89,0.4)] object-cover transform group-hover:scale-105 transition-all duration-300 cursor-pointer"
        />
      </div>
      <h2 className="font-cinzel text-magic-gold text-sm md:text-base tracking-widest uppercase mb-2 opacity-80">
        Grimoire of Six-Faced World
      </h2>
      <h1 className="font-cinzel text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-magic-gold via-yellow-200 to-magic-gold mb-4 text-glow">
        Mushoku Tensei
        <br />
        <span className="text-2xl md:text-4xl mt-1 block text-white/90 font-normal">
          Magic Chants Archive
        </span>
      </h1>
      <p className="text-gray-400 max-w-2xl mx-auto font-light text-sm md:text-base leading-relaxed">
        คลังบทสวดและคำร่ายเวทมนตร์ฉบับสมบูรณ์ คลิกที่การ์ดเพื่อดูรายละเอียดบทสวดเต็ม หรือเข้าสู่โหมดฝึกท่องและเกมประลองเวทมนตร์
      </p>
      <div className="h-px w-32 bg-gradient-to-r from-transparent via-magic-gold to-transparent mx-auto mt-6 opacity-50"></div>

      {/* Navigation Mode Switcher */}
      <div className="flex justify-center items-center gap-3 mt-8 flex-wrap">
        <button
          type="button"
          onClick={() => onTabChange('grimoire')}
          className={`px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border flex items-center gap-2 cursor-pointer ${
            activeTab === 'grimoire'
              ? 'border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]'
              : 'border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold'
          }`}
        >
          <BookMarked className="w-4 h-4" />
          Grimoire Archive
        </button>

        <button
          type="button"
          onClick={() => onTabChange('training')}
          className={`px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border flex items-center gap-2 cursor-pointer ${
            activeTab === 'training'
              ? 'border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]'
              : 'border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold'
          }`}
        >
          <Mic className="w-4 h-4" />
          Chanting Training
        </button>

        <button
          type="button"
          onClick={() => onTabChange('battle')}
          className={`px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border flex items-center gap-2 cursor-pointer ${
            activeTab === 'battle'
              ? 'border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]'
              : 'border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold'
          }`}
        >
          <ShieldAlert className="w-4 h-4" />
          Spell Battle RPG
        </button>
      </div>
    </header>
  );
};
