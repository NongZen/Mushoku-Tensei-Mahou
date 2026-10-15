import React, { useState } from 'react';
import { TabType, Spell } from './types';
import { spellsData } from './data/spells';
import { ParticleCanvas } from './components/ParticleCanvas';
import { Header } from './components/Header';
import { GrimoireView } from './components/GrimoireView';
import { SwordView } from './components/SwordView';
import { TrainingView } from './components/TrainingView';
import { BattleView } from './components/BattleView';
import { SpellModal } from './components/SpellModal';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('grimoire');
  const [selectedSpell, setSelectedSpell] = useState<Spell | null>(null);
  const [trainingSpell, setTrainingSpell] = useState<Spell | null>(null);

  const handlePracticeSpell = (spell: Spell) => {
    setTrainingSpell(spell);
    setActiveTab('training');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="font-prompt min-h-screen relative overflow-x-hidden antialiased text-[#e0e0e0]">
      {/* Ambient Particles Canvas */}
      <ParticleCanvas />

      <div className="container mx-auto px-4 py-8 relative z-10 max-w-7xl">
        {/* Header & Tab navigation */}
        <Header activeTab={activeTab} onTabChange={setActiveTab} />

        {/* View Switcher */}
        <main className="min-h-[500px]">
          {activeTab === 'grimoire' && (
            <GrimoireView
              spells={spellsData}
              onSelectSpell={(spell) => setSelectedSpell(spell)}
            />
          )}

          {activeTab === 'sword' && (
            <SwordView
              spells={spellsData}
              onSelectSpell={(spell) => setSelectedSpell(spell)}
            />
          )}

          {activeTab === 'training' && (
            <TrainingView
              spells={spellsData}
              initialSpell={trainingSpell}
            />
          )}

          {activeTab === 'battle' && (
            <BattleView spells={spellsData} />
          )}
        </main>

        {/* Footer */}
        <footer className="mt-20 text-center text-gray-500 text-sm border-t border-white/10 pt-8 pb-4">
          <p className="font-cinzel">
            &copy; Six-Faced World Grimoire Archive • Mushoku Tensei Chants
          </p>
        </footer>
      </div>

      {/* Spell Details Modal */}
      <SpellModal
        spell={selectedSpell}
        onClose={() => setSelectedSpell(null)}
        onPracticeSpell={handlePracticeSpell}
      />
    </div>
  );
};

export default App;
