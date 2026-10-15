import React, { useState, useMemo } from 'react';
import { Spell } from '../types';
import { Search } from 'lucide-react';

interface SwordViewProps {
  spells: Spell[];
  onSelectSpell: (spell: Spell) => void;
}

type SchoolFilter = 'all' | 'Sword God' | 'Water God' | 'North God';

function getRankWeight(rankStr: string): number {
  const lower = (rankStr || '').toLowerCase();
  if (lower.includes('初・中') || lower.includes('elementary-intermediate')) return 1.5;
  if (lower.includes('初') || lower.includes('elementary') || lower.includes('ต้น')) return 1;
  if (lower.includes('中') || lower.includes('intermediate') || lower.includes('กลาง')) return 2;
  if (lower.includes('上') || lower.includes('advanced') || lower.includes('สูง')) return 3;
  if (lower.includes('聖') || lower.includes('saint') || lower.includes('ศักดิ์สิทธิ์')) return 4;
  if (lower.includes('王') || lower.includes('king') || lower.includes('ราชา')) return 5;
  if (lower.includes('帝') || lower.includes('emperor') || lower.includes('จักรพรรดิ')) return 6;
  if (lower.includes('神') || lower.includes('god') || lower.includes('เทพ') || lower.includes('奥義')) return 7;
  return 3;
}

const schoolOrder: Record<string, number> = {
  'Sword God': 1,
  'Water God': 2,
  'North God': 3,
};

export const SwordView: React.FC<SwordViewProps> = ({ spells, onSelectSpell }) => {
  const [selectedSchool, setSelectedSchool] = useState<SchoolFilter>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortOption, setSortOption] = useState<'school' | 'level' | 'id'>('school');

  // Filter only sword spells
  const swordSpells = useMemo(() => {
    return spells.filter((s) => s.element === 'Sword' || !!s.sword_school);
  }, [spells]);

  const filteredAndSortedSpells = useMemo(() => {
    const query = searchQuery.toLowerCase().trim();

    const filtered = swordSpells.filter((spell) => {
      const matchSchool =
        selectedSchool === 'all' || spell.sword_school === selectedSchool;

      const matchSearch =
        !query ||
        spell.en.toLowerCase().includes(query) ||
        (spell.romaji_name && spell.romaji_name.toLowerCase().includes(query)) ||
        (spell.jp_name && spell.jp_name.includes(query)) ||
        spell.name.toLowerCase().includes(query) ||
        spell.jp.includes(query) ||
        spell.romaji.toLowerCase().includes(query) ||
        spell.th.includes(query) ||
        (spell.sword_school_th && spell.sword_school_th.toLowerCase().includes(query));

      return matchSchool && matchSearch;
    });

    return filtered.sort((a, b) => {
      if (sortOption === 'school') {
        const schoolA = schoolOrder[a.sword_school || ''] || 99;
        const schoolB = schoolOrder[b.sword_school || ''] || 99;
        if (schoolA !== schoolB) return schoolA - schoolB;
        const rankDiff = getRankWeight(a.rank) - getRankWeight(b.rank);
        if (rankDiff !== 0) return rankDiff;
        return a.mp_cost - b.mp_cost;
      }
      if (sortOption === 'level') {
        const rankDiff = getRankWeight(a.rank) - getRankWeight(b.rank);
        if (rankDiff !== 0) return rankDiff;
        return a.mp_cost - b.mp_cost;
      }
      if (sortOption === 'id') {
        return a.id - b.id;
      }
      return 0;
    });
  }, [swordSpells, selectedSchool, searchQuery, sortOption]);

  const getSchoolAccentDot = (school?: string) => {
    switch (school) {
      case 'Sword God':
        return 'bg-red-500 text-red-500';
      case 'Water God':
        return 'bg-cyan-400 text-cyan-400';
      case 'North God':
        return 'bg-emerald-400 text-emerald-400';
      default:
        return 'bg-magic-gold text-magic-gold';
    }
  };

  const swordGodCount = swordSpells.filter((s) => s.sword_school === 'Sword God').length;
  const waterGodCount = swordSpells.filter((s) => s.sword_school === 'Water God').length;
  const northGodCount = swordSpells.filter((s) => s.sword_school === 'North God').length;

  return (
    <section>
      {/* Attached Controls: Top School Pills + Search & Filter Container (Identical to requested UI) */}
      <div className="space-y-4 mb-8">
        {/* Top 4 School Pill Buttons */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <button
            type="button"
            onClick={() => setSelectedSchool('all')}
            className={`py-3 px-4 rounded-xl text-sm font-cinzel font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer border ${
              selectedSchool === 'all'
                ? 'bg-[#c5a059] text-magic-dark border-[#c5a059] shadow-[0_0_15px_rgba(197,160,89,0.4)]'
                : 'bg-black/40 text-gray-300 border-white/10 hover:border-white/30 hover:text-white'
            }`}
          >
            <span>⚔️ ทั้งหมด ({swordSpells.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setSelectedSchool('Sword God')}
            className={`py-3 px-4 rounded-xl text-sm font-cinzel font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer border ${
              selectedSchool === 'Sword God'
                ? 'bg-[#c5a059] text-magic-dark border-[#c5a059] shadow-[0_0_15px_rgba(197,160,89,0.4)]'
                : 'bg-black/40 text-gray-300 border-red-900/50 hover:border-red-500/60 hover:text-white'
            }`}
          >
            <span>🗡️ สำนักเทพดาบ</span>
            <span className="text-xs opacity-75">({swordGodCount})</span>
          </button>

          <button
            type="button"
            onClick={() => setSelectedSchool('Water God')}
            className={`py-3 px-4 rounded-xl text-sm font-cinzel font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer border ${
              selectedSchool === 'Water God'
                ? 'bg-[#c5a059] text-magic-dark border-[#c5a059] shadow-[0_0_15px_rgba(197,160,89,0.4)]'
                : 'bg-black/40 text-gray-300 border-cyan-900/50 hover:border-cyan-500/60 hover:text-white'
            }`}
          >
            <span>🌊 สำนักเทพวารี</span>
            <span className="text-xs opacity-75">({waterGodCount})</span>
          </button>

          <button
            type="button"
            onClick={() => setSelectedSchool('North God')}
            className={`py-3 px-4 rounded-xl text-sm font-cinzel font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer border ${
              selectedSchool === 'North God'
                ? 'bg-[#c5a059] text-magic-dark border-[#c5a059] shadow-[0_0_15px_rgba(197,160,89,0.4)]'
                : 'bg-black/40 text-gray-300 border-emerald-900/50 hover:border-emerald-500/60 hover:text-white'
            }`}
          >
            <span>🌿 สำนักเทพอุดร</span>
            <span className="text-xs opacity-75">({northGodCount})</span>
          </button>
        </div>

        {/* Search, Sort & School Select Bar (Div as specified in focus mode & image) */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 bg-magic-blue/40 p-4 rounded-xl border border-magic-gold/20 backdrop-blur-sm z-20 relative shadow-[0_4px_20px_rgba(0,0,0,0.5)]">
          {/* Search Box */}
          <div className="relative w-full md:w-80">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="ค้นหากระบวนท่าดาบ (Search)..."
              className="w-full bg-magic-dark/80 border border-magic-gold/30 rounded-lg py-2 pl-9 pr-4 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-magic-gold focus:ring-1 focus:ring-magic-gold font-prompt"
            />
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-gray-400" />
          </div>

          {/* Sort & School Dropdowns */}
          <div className="flex flex-wrap md:flex-nowrap gap-4 w-full md:w-auto items-center">
            {/* Sort Select */}
            <div className="flex items-center gap-2 w-full md:w-auto">
              <label htmlFor="sword-sort-select" className="text-gray-400 font-cinzel text-xs uppercase tracking-wider whitespace-nowrap">
                SORT BY:
              </label>
              <select
                id="sword-sort-select"
                value={sortOption}
                onChange={(e) => setSortOption(e.target.value as 'school' | 'level' | 'id')}
                className="w-full md:w-56 py-2 pl-4 pr-8 rounded-lg cursor-pointer font-prompt text-sm transition-all bg-magic-dark/80 border border-magic-gold/30 text-gray-200 focus:outline-none focus:border-magic-gold"
              >
                <option value="school">เรียงตามสำนักและขั้น (School & Rank)</option>
                <option value="level">เรียงตามลำดับขั้น (Tier / Rank)</option>
                <option value="id">ลำดับตาม ID ดั้งเดิม (Original ID)</option>
              </select>
            </div>

            {/* School Filter Dropdown */}
            <div className="flex items-center gap-2 w-full md:w-auto">
              <label htmlFor="sword-school-select" className="text-gray-400 font-cinzel text-xs uppercase tracking-wider whitespace-nowrap">
                SCHOOL:
              </label>
              <select
                id="sword-school-select"
                value={selectedSchool}
                onChange={(e) => setSelectedSchool(e.target.value as SchoolFilter)}
                className="w-full md:w-52 py-2 pl-4 pr-8 rounded-lg cursor-pointer font-prompt text-sm transition-all bg-magic-dark/80 border border-magic-gold/30 text-gray-200 focus:outline-none focus:border-magic-gold"
              >
                <option value="all">ทุกสำนักดาบ (All Styles)</option>
                <option value="Sword God">สำนักเทพดาบ (Sword God)</option>
                <option value="Water God">สำนักเทพวารี (Water God)</option>
                <option value="North God">สำนักเทพอุดร (North God)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Sword Cards Grid - FORMATTED IDENTICALLY TO GRIMOIRE GALLERY */}
      {filteredAndSortedSpells.length === 0 ? (
        <div className="col-span-full text-center text-gray-500 py-16 font-cinzel text-xl">
          ไม่พบกระบวนท่าดาบที่ค้นหา (No sword techniques found matching the criteria)
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 transition-all duration-300">
          {filteredAndSortedSpells.map((spell) => {
            const accentClasses = getSchoolAccentDot(spell.sword_school);
            return (
              <div
                key={spell.id}
                onClick={() => onSelectSpell(spell)}
                className="spell-card rounded-xl p-6 relative overflow-hidden flex flex-col h-full group cursor-pointer"
              >
                <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-white/5 to-transparent rounded-bl-full pointer-events-none" />

                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center">
                    <div className={`w-2 h-2 rounded-full mr-2.5 shadow-[0_0_8px_currentColor] ${accentClasses}`} />
                    <span className="text-xs text-gray-400 uppercase tracking-wider font-semibold font-prompt">
                      {spell.rank}
                    </span>
                  </div>
                  <span className="text-[10px] text-magic-gold/80 font-cinzel px-2 py-0.5 rounded bg-magic-gold/10 border border-magic-gold/20">
                    {spell.sword_school_th || 'วิชาดาบ'}
                  </span>
                </div>

                <h3 className="font-cinzel text-2xl font-bold text-magic-gold-light mb-0.5 group-hover:text-magic-gold transition-colors">
                  {spell.en}
                </h3>
                <h4 className="text-magic-gold-light/90 text-sm mb-4 font-medium tracking-wide">
                  {spell.romaji_name} <span className="text-gray-500 text-xs font-jp">({spell.jp_name})</span>
                </h4>

                <div className="mt-auto">
                  <p className="text-gray-300 text-xs sm:text-sm line-clamp-3 italic opacity-85 border-l-2 border-magic-gold/30 pl-3">
                    "{spell.romaji}"
                  </p>
                </div>

                <div className="absolute bottom-4 right-4 w-1 h-1 bg-magic-gold rounded-full opacity-0 group-hover:opacity-100 animate-ping" />
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
};
