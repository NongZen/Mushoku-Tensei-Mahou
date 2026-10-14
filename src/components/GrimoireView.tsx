import React, { useState, useMemo } from 'react';
import { Spell } from '../types';
import { Search } from 'lucide-react';

interface GrimoireViewProps {
  spells: Spell[];
  onSelectSpell: (spell: Spell) => void;
}

const elementOrder: Record<string, number> = {
  Water: 1,
  Fire: 2,
  Earth: 3,
  Healing: 4,
  Dragon: 5,
};

function getSpellRankWeight(rankStr: string): number {
  const lower = (rankStr || '').toLowerCase();
  if (lower.includes('初・中') || lower.includes('elementary-intermediate')) return 1.5;
  if (lower.includes('初') || lower.includes('elementary')) return 1;
  if (lower.includes('中') || lower.includes('intermediate')) return 2;
  if (lower.includes('上') || lower.includes('advanced')) return 3;
  if (lower.includes('聖') || lower.includes('saint')) return 4;
  if (lower.includes('王') || lower.includes('king')) return 5;
  if (lower.includes('帝') || lower.includes('emperor')) return 6;
  if (lower.includes('神') || lower.includes('god') || lower.includes('ancient') || lower.includes('unique')) return 7;
  return 3;
}

export const GrimoireView: React.FC<GrimoireViewProps> = ({ spells, onSelectSpell }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortOption, setSortOption] = useState<'element' | 'level' | 'id'>('element');
  const [filterOption, setFilterOption] = useState<string>('all');

  const filteredAndSortedSpells = useMemo(() => {
    const query = searchQuery.toLowerCase().trim();

    const filtered = spells.filter((spell) => {
      const matchFilter = filterOption === 'all' || spell.element.toLowerCase() === filterOption.toLowerCase();
      const matchSearch =
        !query ||
        spell.en.toLowerCase().includes(query) ||
        (spell.romaji_name && spell.romaji_name.toLowerCase().includes(query)) ||
        (spell.jp_name && spell.jp_name.includes(query)) ||
        spell.name.toLowerCase().includes(query) ||
        spell.jp.includes(query) ||
        spell.romaji.toLowerCase().includes(query) ||
        spell.th.includes(query);

      return matchFilter && matchSearch;
    });

    return filtered.sort((a, b) => {
      if (sortOption === 'element') {
        const elemDiff = (elementOrder[a.element] || 99) - (elementOrder[b.element] || 99);
        if (elemDiff !== 0) return elemDiff;
        const rankDiff = getSpellRankWeight(a.rank) - getSpellRankWeight(b.rank);
        if (rankDiff !== 0) return rankDiff;
        return a.mp_cost - b.mp_cost;
      }
      if (sortOption === 'level') {
        const rankDiff = getSpellRankWeight(a.rank) - getSpellRankWeight(b.rank);
        if (rankDiff !== 0) return rankDiff;
        return a.mp_cost - b.mp_cost;
      }
      if (sortOption === 'id') {
        return a.id - b.id;
      }
      return 0;
    });
  }, [spells, searchQuery, sortOption, filterOption]);

  const getAccentDot = (element: string) => {
    switch (element) {
      case 'Water':
        return 'bg-blue-500 text-blue-500';
      case 'Fire':
        return 'bg-red-500 text-red-500';
      case 'Earth':
        return 'bg-amber-700 text-amber-700';
      case 'Healing':
        return 'bg-yellow-400 text-yellow-400';
      case 'Dragon':
        return 'bg-rose-500 text-rose-500';
      default:
        return 'bg-gray-500 text-gray-500';
    }
  };

  return (
    <section>
      {/* Controls (Search, Sort & Filter) */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4 bg-magic-blue/40 p-4 rounded-xl border border-magic-gold/20 backdrop-blur-sm z-20 relative shadow-[0_4px_20px_rgba(0,0,0,0.5)]">
        {/* Search Box */}
        <div className="relative w-full md:w-72">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="ค้นหาเวทมนตร์ (Search)..."
            className="w-full bg-magic-dark/80 border border-magic-gold/30 rounded-lg py-2 pl-9 pr-4 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-magic-gold focus:ring-1 focus:ring-magic-gold"
          />
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-gray-400" />
        </div>

        <div className="flex flex-wrap md:flex-nowrap gap-4 w-full md:w-auto">
          <div className="flex items-center gap-3 w-full md:w-auto">
            <label htmlFor="sort-select" className="text-gray-400 font-cinzel text-xs uppercase tracking-wider whitespace-nowrap">
              Sort By:
            </label>
            <select
              id="sort-select"
              value={sortOption}
              onChange={(e) => setSortOption(e.target.value as 'element' | 'level' | 'id')}
              className="w-full md:w-56 py-2 pl-4 pr-10 rounded-lg cursor-pointer font-prompt text-sm transition-all"
            >
              <option value="element">เรียงตามธาตุและขั้น (Element & Tier)</option>
              <option value="level">เรียงตามลำดับขั้น (Tier / Level)</option>
              <option value="id">ลำดับตาม ID ดั้งเดิม (Original ID)</option>
            </select>
          </div>

          <div className="flex items-center gap-3 w-full md:w-auto">
            <label htmlFor="filter-select" className="text-gray-400 font-cinzel text-xs uppercase tracking-wider whitespace-nowrap">
              Filter:
            </label>
            <select
              id="filter-select"
              value={filterOption}
              onChange={(e) => setFilterOption(e.target.value)}
              className="w-full md:w-44 py-2 pl-4 pr-10 rounded-lg cursor-pointer font-prompt text-sm transition-all"
            >
              <option value="all">ทั้งหมด (All)</option>
              <option value="Water">น้ำ / น้ำแข็ง (Water/Ice)</option>
              <option value="Fire">ไฟ (Fire)</option>
              <option value="Earth">ดิน (Earth)</option>
              <option value="Healing">รักษา / ศักดิ์สิทธิ์ (Healing)</option>
              <option value="Dragon">มังกร / อัญเชิญ (Dragon)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Grimoire Cards Grid */}
      {filteredAndSortedSpells.length === 0 ? (
        <div className="col-span-full text-center text-gray-500 py-16 font-cinzel text-xl">
          No spells found matching the criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 transition-all duration-300">
          {filteredAndSortedSpells.map((spell) => {
            const accentClasses = getAccentDot(spell.element);
            return (
              <div
                key={spell.id}
                onClick={() => onSelectSpell(spell)}
                className="spell-card rounded-xl p-6 relative overflow-hidden flex flex-col h-full group"
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
                    {spell.element}
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
