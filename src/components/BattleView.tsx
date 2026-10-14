import React, { useState, useEffect, useRef } from 'react';
import { Spell, Enemy, BattleState } from '../types';
import { enemiesData } from '../data/spells';
import { findMatchingSpell } from '../utils/chantEvaluator';
import {
  RotateCcw,
  Mic,
  Volume2,
  Sparkles,
  Trophy,
  Skull,
  Zap,
  BookOpen,
  Send,
  HelpCircle,
} from 'lucide-react';

interface BattleViewProps {
  spells: Spell[];
}

export const BattleView: React.FC<BattleViewProps> = ({ spells }) => {
  const [enemyKey, setEnemyKey] = useState<string>('crawler');
  const [battleState, setBattleState] = useState<BattleState>(() => {
    const initialEnemy = enemiesData['crawler'];
    return {
      playerHp: 500,
      playerMaxHp: 500,
      playerMp: 350,
      playerMaxMp: 350,
      turn: 1,
      enemyKey: 'crawler',
      enemy: { ...initialEnemy },
      comboWet: false,
      comboDefDown: false,
    };
  });

  const [logs, setLogs] = useState<string[]>([
    '[SYSTEM] Combat started! Select Quick Cast to fire immediately, or speak/type any spell in Japanese or Thai.',
  ]);

  // Chanting Phase Modal state (only for full chant immersion, NOT for Quick Cast!)
  const [pendingChantSpell, setPendingChantSpell] = useState<Spell | null>(null);
  const [isChantRecording, setIsChantRecording] = useState<boolean>(false);
  const [chantLang, setChantLang] = useState<'ja-JP' | 'th-TH'>('ja-JP');
  const [chantTranscript, setChantTranscript] = useState<string>('');
  const [chantTypedText, setChantTypedText] = useState<string>('');

  // Quick Cast Bar state (Speech & Typing in JP / TH with NO Chanting Phase modal)
  const [quickInputText, setQuickInputText] = useState<string>('');
  const [quickVoiceLang, setQuickVoiceLang] = useState<'ja-JP' | 'th-TH'>('th-TH');
  const [isQuickListening, setIsQuickListening] = useState<boolean>(false);
  const [quickHeardNotice, setQuickHeardNotice] = useState<string>('');

  const [gameOver, setGameOver] = useState<'victory' | 'defeat' | null>(null);

  const logContainerRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll combat log
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const initBattle = (key: string = enemyKey) => {
    const e = enemiesData[key] || enemiesData['crawler'];
    setBattleState({
      playerHp: 500,
      playerMaxHp: 500,
      playerMp: 350,
      playerMaxMp: 350,
      turn: 1,
      enemyKey: key,
      enemy: { ...e },
      comboWet: false,
      comboDefDown: false,
    });
    setLogs([
      `[SYSTEM] Combat started with ${e.name}! Select Quick Cast ⚡ or Chant 📜. Speak or type in JP / TH.`,
    ]);
    setGameOver(null);
    setPendingChantSpell(null);
    setIsChantRecording(false);
    setIsQuickListening(false);
    setQuickHeardNotice('');
  };

  const handleEnemyChange = (eKey: string) => {
    setEnemyKey(eKey);
    initBattle(eKey);
  };

  const battleSpellIds = [2, 8, 12, 16, 20, 21, 5, 1];
  const battleSpells = spells.filter((s) => battleSpellIds.includes(s.id));

  const addLog = (msg: string) => {
    setLogs((prev) => [...prev, msg]);
  };

  // CORE CAST EXECUTION (Directly executed for Quick Cast without any modal popup!)
  const executeCast = (spell: Spell, castTypeLabel: string = 'Quick Cast') => {
    if (gameOver) return;

    if (battleState.playerMp < spell.mp_cost) {
      addLog(`[WARNING] Not enough MP to cast ${spell.en} (Need ${spell.mp_cost} MP, have ${battleState.playerMp} MP)`);
      return;
    }

    setPendingChantSpell(null);
    setIsChantRecording(false);
    setIsQuickListening(false);

    setBattleState((prev) => {
      const nextMp = Math.max(0, prev.playerMp - spell.mp_cost);
      let nextPlayerHp = prev.playerHp;
      let nextEnemyHp = prev.enemy.hp;
      let comboWet = prev.comboWet;

      if (spell.type === 'heal') {
        const healAmt = spell.power * 2;
        nextPlayerHp = Math.min(prev.playerMaxHp, prev.playerHp + healAmt);
        addLog(`[CAST - ${castTypeLabel}] You cast ${spell.en} (${spell.name.split('(')[0].trim()})! Restored ${healAmt} HP.`);
      } else {
        const dmg = spell.power;
        let multiplier = 1.0;

        // Elemental Weakness
        if (
          prev.enemy.weak.includes(spell.element) ||
          prev.enemy.weak.includes(spell.en)
        ) {
          multiplier += 0.5;
          addLog(`[WEAKNESS] ${prev.enemy.name} is weak against ${spell.element}! (1.5x Dmg)`);
        }

        // Combo System: Water Splash + Ice = Freeze Shatter!
        if (spell.en === 'Water Splash') {
          comboWet = true;
          addLog(`[COMBO READY] Target is drenched in water! Follow with Ice to Shatter!`);
        } else if (comboWet && (spell.en.includes('Ice') || spell.element === 'Water')) {
          multiplier += 0.8;
          comboWet = false;
          addLog(`[FROST COMBO] SHATTER! Drenched foe frozen and fractured! (+80% Dmg)`);
        }

        const totalDmg = Math.round(dmg * multiplier);
        nextEnemyHp = Math.max(0, prev.enemy.hp - totalDmg);
        addLog(`[DAMAGE - ${castTypeLabel}] You hit ${prev.enemy.name} with ${spell.en} (${spell.jp_name || spell.name}) for ${totalDmg} damage!`);
      }

      if (nextEnemyHp <= 0) {
        addLog(`[VICTORY] You defeated ${prev.enemy.name}! Final Grade: S-RANK MAGUS!`);
        setGameOver('victory');
        return {
          ...prev,
          playerHp: nextPlayerHp,
          playerMp: nextMp,
          enemy: { ...prev.enemy, hp: 0 },
          comboWet,
        };
      }

      // Schedule enemy counter-turn
      setTimeout(() => {
        handleEnemyTurn();
      }, 800);

      return {
        ...prev,
        playerHp: nextPlayerHp,
        playerMp: nextMp,
        enemy: { ...prev.enemy, hp: nextEnemyHp },
        comboWet,
      };
    });
  };

  const handleEnemyTurn = () => {
    setBattleState((prev) => {
      if (prev.enemy.hp <= 0 || prev.playerHp <= 0) return prev;

      const dmg = prev.enemy.atk + Math.floor(Math.random() * 15);
      const nextPlayerHp = Math.max(0, prev.playerHp - dmg);
      const nextPlayerMp = Math.min(prev.playerMaxMp, prev.playerMp + 15);
      const nextTurn = prev.turn + 1;

      addLog(`[ENEMY] ${prev.enemy.name} attacks you for ${dmg} physical damage! (+15 Mana restored)`);

      if (nextPlayerHp <= 0) {
        addLog(`[DEFEAT] Rudeus has fallen. Grade: F`);
        setGameOver('defeat');
      }

      return {
        ...prev,
        playerHp: nextPlayerHp,
        playerMp: nextPlayerMp,
        turn: nextTurn,
      };
    });
  };

  // QUICK CAST DIRECTLY: NO CHANTING PHASE MODAL!
  const handleQuickCastSlot = (spell: Spell) => {
    // If Quick Cast is pressed, do NOT open any Chanting Phase modal!
    executeCast(spell, 'Quick Cast ⚡');
  };

  // QUICK VOICE/TEXT CAST (Searches across JP/TH/EN and immediately casts with NO modal!)
  const handleQuickCastByText = (input: string) => {
    const matched = findMatchingSpell(input, spells);
    if (matched) {
      setQuickInputText('');
      setQuickHeardNotice(`Matched: ${matched.en} (${matched.name.split('(')[0]})`);
      executeCast(matched, `Quick Cast [${input}]`);
    } else {
      setQuickHeardNotice(`ไม่พบเวทมนตร์จากคำว่า "${input}". ลองพูดหรือพิมพ์ชื่อเวท เช่น วอเตอร์บอล, Fireball, ヒーリング`);
    }
  };

  const toggleQuickVoice = () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setQuickHeardNotice('เบราว์เซอร์ไม่รองรับไมค์ กรุณาพิมพ์ชื่อเวทแทน');
      return;
    }

    if (isQuickListening) {
      setIsQuickListening(false);
    } else {
      try {
        const recognition = new SpeechRecognition();
        recognition.lang = quickVoiceLang;
        recognition.interimResults = false;
        recognition.continuous = false;

        setIsQuickListening(true);
        setQuickHeardNotice(`Listening (${quickVoiceLang === 'th-TH' ? 'ภาษาไทย' : 'Japanese'})... พูดชื่อเวทมนตร์ทันที!`);

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        recognition.onresult = (e: any) => {
          const heard = e.results[0][0].transcript;
          setIsQuickListening(false);
          setQuickHeardNotice(`Heard: "${heard}"`);
          handleQuickCastByText(heard);
        };

        recognition.onerror = (err: any) => {
          setIsQuickListening(false);
          setQuickHeardNotice(`Mic notice: ${err.error || 'ended'}`);
        };

        recognition.onend = () => {
          setIsQuickListening(false);
        };

        recognition.start();
      } catch (e) {
        console.warn(e);
        setIsQuickListening(false);
      }
    }
  };

  // SMART QUICK CAST: Finds and casts best spell immediately without modal!
  const handleSmartQuickCast = () => {
    // Find spell that targets enemy weakness and player can afford
    const affordableSpells = battleSpells.filter((s) => battleState.playerMp >= s.mp_cost);
    if (affordableSpells.length === 0) {
      addLog('[WARNING] Not enough MP for any battle spell! Take damage to recover mana or use low tier.');
      return;
    }

    // If player HP is critical (< 150), prioritize healing
    if (battleState.playerHp < 150) {
      const healSpell = affordableSpells.find((s) => s.type === 'heal');
      if (healSpell) {
        executeCast(healSpell, 'Quick Cast Auto-Heal ⚡');
        return;
      }
    }

    // If combo wet is active, prioritize Ice spell
    if (battleState.comboWet) {
      const iceSpell = affordableSpells.find((s) => s.en.includes('Ice') || s.en.includes('Icicle'));
      if (iceSpell) {
        executeCast(iceSpell, 'Quick Cast Frost Combo ⚡');
        return;
      }
    }

    // Weakness counter
    const weakSpell = affordableSpells.find(
      (s) =>
        battleState.enemy.weak.includes(s.element) ||
        battleState.enemy.weak.includes(s.en)
    );
    if (weakSpell) {
      executeCast(weakSpell, 'Quick Cast Weakness Counter ⚡');
      return;
    }

    // Default highest power affordable
    affordableSpells.sort((a, b) => b.power - a.power);
    executeCast(affordableSpells[0], 'Quick Cast Tactical ⚡');
  };

  // OPEN CHANTING PHASE MODAL (Only when user explicitly chooses "Chant & Cast")
  const openChantingModal = (spell: Spell) => {
    setPendingChantSpell(spell);
    setChantTranscript('');
    setChantTypedText('');
    setIsChantRecording(false);
  };

  const toggleChantSpeech = () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setChantTranscript('ไมโครโฟนไม่พร้อมใช้งาน สามารถพิมพ์บทร่ายเพื่อร่ายเวทได้');
      return;
    }

    if (isChantRecording) {
      setIsChantRecording(false);
    } else {
      try {
        const recognition = new SpeechRecognition();
        recognition.lang = chantLang;
        recognition.interimResults = true;
        recognition.continuous = false;

        setIsChantRecording(true);
        setChantTranscript(`Listening (${chantLang === 'th-TH' ? 'ภาษาไทย' : 'Japanese'})...`);

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        recognition.onresult = (e: any) => {
          let heard = '';
          for (let i = e.resultIndex; i < e.results.length; ++i) {
            heard += e.results[i][0].transcript;
          }
          setChantTranscript(`Heard: "${heard}"`);

          if (pendingChantSpell) {
            const jpTrigger = (pendingChantSpell.jp_name || pendingChantSpell.en).toLowerCase();
            const thTrigger = pendingChantSpell.name.split('(')[0].trim().toLowerCase();
            const clean = heard.toLowerCase();

            if (clean.includes(jpTrigger) || clean.includes(thTrigger) || clean.length >= 6) {
              recognition.stop();
              setIsChantRecording(false);
              executeCast(pendingChantSpell, `Chant Recited (${chantLang === 'th-TH' ? 'ไทย' : 'JP'}) 📜`);
            }
          }
        };

        recognition.onerror = () => {
          setIsChantRecording(false);
        };

        recognition.onend = () => {
          setIsChantRecording(false);
        };

        recognition.start();
      } catch {
        setIsChantRecording(false);
      }
    }
  };

  const handleChantTypeCast = (e: React.FormEvent) => {
    e.preventDefault();
    if (!pendingChantSpell) return;
    executeCast(pendingChantSpell, `Chant Typed (${chantTypedText || 'Manual'}) 📜`);
  };

  const currentEnemyInfo = (enemiesData[enemyKey] || enemiesData['crawler']) as Enemy;

  return (
    <section>
      <div className="bg-gradient-to-b from-[#111a24] to-[#0d121c] border-2 border-magic-gold/40 rounded-3xl p-6 md:p-8 backdrop-blur-md max-w-5xl mx-auto shadow-2xl">
        {/* Battle Top Header */}
        <div className="flex flex-col sm:flex-row justify-between items-center pb-4 mb-6 border-b border-magic-gold/20 gap-3">
          <div>
            <span className="text-xs uppercase tracking-widest text-magic-gold font-cinzel">
              Turn-Based Arena • JP / TH Voice & Typing
            </span>
            <h2 className="font-cinzel text-2xl font-bold text-white">
              Labyrinth Battle Simulator
            </h2>
          </div>
          <div className="flex items-center gap-3">
            <label className="text-xs text-gray-400 font-cinzel uppercase">
              Enemy:
            </label>
            <select
              value={enemyKey}
              onChange={(e) => handleEnemyChange(e.target.value)}
              className="py-1.5 px-3 rounded-lg text-xs"
            >
              <option value="crawler">Iron Crawler (Weak: Ice/Lightning)</option>
              <option value="treant">Forest Treant (Weak: Fire)</option>
              <option value="salamander">Magma Salamander (Weak: Water)</option>
              <option value="wyvern">Red Wyvern (Weak: Cumulonimbus/Dragon)</option>
            </select>
            <button
              type="button"
              onClick={() => initBattle(enemyKey)}
              className="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-magic-gold/30 text-xs text-magic-gold cursor-pointer transition-colors"
              title="Restart Battle"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Combatants Status Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Player */}
          <div className="bg-black/40 border border-magic-gold/20 rounded-xl p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-cinzel text-white font-bold flex items-center gap-2">
                <span className="text-blue-400">🧙‍♂️</span> Rudeus (Mage)
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-cinzel">
                Ready
              </span>
            </div>

            <div className="flex justify-between text-xs text-gray-400 mb-1">
              <span>
                HP: <strong className="text-white">{battleState.playerHp} / {battleState.playerMaxHp}</strong>
              </span>
              {battleState.comboWet && (
                <span className="text-cyan-400 text-[10px] animate-pulse">💧 Water Drenched Primed</span>
              )}
            </div>
            <div className="w-full bg-black/60 rounded-full h-3 border border-gray-700 overflow-hidden mb-3">
              <div
                className="bg-gradient-to-r from-red-500 to-green-500 h-full rounded-full transition-all duration-300"
                style={{
                  width: `${(battleState.playerHp / battleState.playerMaxHp) * 100}%`,
                }}
              />
            </div>

            <div className="flex justify-between text-xs text-gray-400 mb-1">
              <span>
                MP: <strong className="text-blue-300">{battleState.playerMp} / {battleState.playerMaxMp}</strong>
              </span>
            </div>
            <div className="w-full bg-black/60 rounded-full h-3 border border-gray-700 overflow-hidden">
              <div
                className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full transition-all duration-300"
                style={{
                  width: `${(battleState.playerMp / battleState.playerMaxMp) * 100}%`,
                }}
              />
            </div>
          </div>

          {/* Enemy */}
          <div className="bg-black/40 border border-magic-gold/20 rounded-xl p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-cinzel text-white font-bold flex items-center gap-2">
                <Skull className="w-4 h-4 text-red-400" />
                {battleState.enemy.name}
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-red-500/20 text-red-300 font-cinzel">
                {battleState.enemy.type}
              </span>
            </div>

            <div className="flex justify-between text-xs text-gray-400 mb-1">
              <span>
                Enemy HP: <strong className="text-white">{battleState.enemy.hp} / {battleState.enemy.maxHp}</strong>
              </span>
              <span className="text-xs text-cyan-400 font-medium">
                Weak: {battleState.enemy.weak.join(', ')}
              </span>
            </div>
            <div className="w-full bg-black/60 rounded-full h-3 border border-gray-700 overflow-hidden mb-3">
              <div
                className="bg-gradient-to-r from-red-600 to-green-500 h-full rounded-full transition-all duration-300"
                style={{
                  width: `${(battleState.enemy.hp / battleState.enemy.maxHp) * 100}%`,
                }}
              />
            </div>

            <div className="text-xs text-gray-400">
              {currentEnemyInfo.desc || 'Dangerous beast encountered in the depths of the teleport labyrinth.'}
            </div>
          </div>
        </div>

        {/* Combat Log */}
        <div
          ref={logContainerRef}
          className="bg-black/60 border border-gray-800 rounded-xl p-4 text-xs md:text-sm text-gray-300 h-32 overflow-y-auto mb-6 leading-relaxed font-mono"
        >
          {logs.map((log, index) => (
            <div
              key={index}
              className={
                log.includes('[VICTORY]')
                  ? 'text-green-400 font-bold'
                  : log.includes('[DEFEAT]')
                  ? 'text-red-400 font-bold'
                  : log.includes('[WEAKNESS]') || log.includes('[FROST COMBO]')
                  ? 'text-cyan-300 font-semibold'
                  : log.includes('[ENEMY]')
                  ? 'text-amber-300'
                  : log.includes('[WARNING]')
                  ? 'text-red-300'
                  : 'text-gray-300'
              }
            >
              {log}
            </div>
          ))}
        </div>

        {/* QUICK CAST BAR (Speech & Type in JP / TH -> NO CHANTING PHASE MODAL!) */}
        <div className="bg-black/40 border border-magic-gold/30 rounded-2xl p-4 mb-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-3">
            <span className="text-xs uppercase font-cinzel text-magic-gold tracking-wider flex items-center gap-1.5 font-bold">
              <Zap className="w-3.5 h-3.5 fill-current" /> Quick Cast Center (ไม่มี Chanting Phase • พูดหรือพิมพ์ร่ายได้ทันที)
            </span>

            {/* Quick Lang Switcher & Auto Button */}
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setQuickVoiceLang((prev) => (prev === 'th-TH' ? 'ja-JP' : 'th-TH'))}
                className="px-2.5 py-1 rounded bg-white/5 border border-white/20 text-[11px] text-gray-300 hover:text-white flex items-center gap-1 font-cinzel cursor-pointer"
                title="สลับภาษาพูด Quick Voice Cast"
              >
                <span>🌐 {quickVoiceLang === 'th-TH' ? '🇹🇭 ไทย (th-TH)' : '🇯🇵 日本語 (ja-JP)'}</span>
              </button>

              <button
                type="button"
                onClick={handleSmartQuickCast}
                className="px-3 py-1 bg-gradient-to-r from-magic-gold to-yellow-500 text-magic-dark font-cinzel font-bold text-xs uppercase tracking-wider rounded-lg hover:scale-105 transition-transform cursor-pointer shadow-[0_0_10px_rgba(197,160,89,0.3)] flex items-center gap-1"
                title="ระบบวิเคราะห์จุดอ่อนแล้วร่ายเวทที่ดีที่สุดทันทีโดยไม่ต้องผ่าน Chanting Phase"
              >
                <Sparkles className="w-3 h-3" /> Quick Cast Smart ⚡
              </button>
            </div>
          </div>

          <div className="flex gap-2">
            <button
              type="button"
              onClick={toggleQuickVoice}
              className={`px-3 py-2 rounded-xl border flex items-center justify-center transition-all cursor-pointer ${
                isQuickListening
                  ? 'recording-pulse'
                  : 'bg-white/5 border-magic-gold/40 text-magic-gold hover:bg-magic-gold/20'
              }`}
              title="พูดชื่อเวทเพื่อร่ายทันที (ไม่ต้องผ่าน Chanting Phase)"
            >
              <Mic className="w-4 h-4" />
            </button>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (quickInputText.trim()) handleQuickCastByText(quickInputText);
              }}
              className="flex-1 flex gap-2"
            >
              <input
                type="text"
                value={quickInputText}
                onChange={(e) => setQuickInputText(e.target.value)}
                placeholder="พิมพ์ชื่อเวท เช่น วอเตอร์บอล, Fireball, ヒーリング, ฮีลลิ่ง เพื่อ Quick Cast ทันที..."
                className="flex-1 bg-black/60 border border-white/15 rounded-xl px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-magic-gold font-prompt"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-magic-gold/20 hover:bg-magic-gold/30 border border-magic-gold text-magic-gold text-xs font-cinzel font-bold uppercase rounded-xl transition-all cursor-pointer flex items-center gap-1"
              >
                <Send className="w-3.5 h-3.5" /> Cast ⚡
              </button>
            </form>
          </div>

          {quickHeardNotice && (
            <div className="mt-2 text-[11px] text-magic-gold-light italic">
              {quickHeardNotice}
            </div>
          )}
        </div>

        {/* Spell Action Slots Header */}
        <div className="flex justify-between items-center mb-3">
          <span className="text-xs uppercase font-cinzel text-magic-gold tracking-wider">
            Turn: <strong className="text-white">{battleState.turn}</strong> • Spell Action Slots (เลือก Quick Cast ⚡ หรือ Chant 📜)
          </span>
          <div className="text-[11px] text-gray-400 flex items-center gap-1">
            <HelpCircle className="w-3.5 h-3.5 text-magic-gold" />
            <span>กด "Quick Cast ⚡" จะยิงเวททันทีโดยไม่มี Chanting Phase</span>
          </div>
        </div>

        {/* Spell Action Slots Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
          {battleSpells.map((s) => {
            const canAfford = battleState.playerMp >= s.mp_cost;
            return (
              <div
                key={s.id}
                className={`bg-black/50 border border-magic-gold/30 rounded-xl p-3 flex flex-col justify-between transition-all ${
                  !canAfford || gameOver ? 'opacity-40' : 'hover:border-magic-gold'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs font-bold text-white font-cinzel">{s.en}</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/20 text-cyan-300 font-cinzel">
                    {s.mp_cost} MP
                  </span>
                </div>
                <div className="text-[11px] text-magic-gold-light font-prompt mb-1 truncate">
                  {s.name.split('(')[0].trim()}
                </div>
                <div className="text-[10px] text-gray-400 mb-3 flex justify-between">
                  <span>PWR: {s.power}</span>
                  <span className="text-magic-gold">{s.element}</span>
                </div>

                {/* DUAL ACTION BUTTONS: QUICK CAST vs CHANT */}
                <div className="grid grid-cols-2 gap-1.5 mt-auto pt-2 border-t border-white/5">
                  <button
                    type="button"
                    disabled={!canAfford || !!gameOver}
                    onClick={() => handleQuickCastSlot(s)}
                    className="py-1.5 px-2 bg-gradient-to-r from-magic-gold to-yellow-500 text-magic-dark font-cinzel font-bold text-[11px] uppercase rounded-lg hover:scale-[1.02] transition-transform disabled:opacity-30 disabled:pointer-events-none cursor-pointer flex items-center justify-center gap-1"
                    title="Quick Cast ทันที ไม่ต้องมี Chanting Phase"
                  >
                    <Zap className="w-3 h-3 fill-current" /> Quick ⚡
                  </button>

                  <button
                    type="button"
                    disabled={!canAfford || !!gameOver}
                    onClick={() => openChantingModal(s)}
                    className="py-1.5 px-2 bg-white/5 hover:bg-white/10 text-gray-300 border border-white/10 font-cinzel text-[11px] uppercase rounded-lg disabled:opacity-30 disabled:pointer-events-none cursor-pointer flex items-center justify-center gap-1"
                    title="เข้าสู่โหมดท่องบทสวดเต็มรูปแบบ"
                  >
                    <BookOpen className="w-3 h-3" /> Chant 📜
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* Victory/Defeat Banner */}
        {gameOver && (
          <div className="mt-4 p-4 rounded-xl border text-center backdrop-blur-md bg-black/80">
            {gameOver === 'victory' ? (
              <div className="space-y-2">
                <Trophy className="w-8 h-8 mx-auto text-yellow-400" />
                <h4 className="font-cinzel text-xl font-bold text-yellow-400">
                  VICTORY! S-RANK MAGUS
                </h4>
                <p className="text-xs text-gray-300">
                  {battleState.enemy.name} has been defeated. Your incantation mastery prevails!
                </p>
                <button
                  type="button"
                  onClick={() => initBattle(enemyKey)}
                  className="mt-2 px-6 py-2 rounded-full bg-magic-gold text-magic-dark font-cinzel font-bold text-xs uppercase hover:bg-yellow-400 cursor-pointer"
                >
                  Battle Again
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                <Skull className="w-8 h-8 mx-auto text-red-500" />
                <h4 className="font-cinzel text-xl font-bold text-red-400">
                  DEFEATED IN LABYRINTH
                </h4>
                <p className="text-xs text-gray-300">
                  You ran out of health. Regroup, manage your MP and combine elements!
                </p>
                <button
                  type="button"
                  onClick={() => initBattle(enemyKey)}
                  className="mt-2 px-6 py-2 rounded-full bg-red-600 text-white font-cinzel font-bold text-xs uppercase hover:bg-red-500 cursor-pointer"
                >
                  Try Again
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* CHANTING PHASE MODAL (ONLY OPENED WHEN USER EXPLICITLY CLICKS "Chant 📜", NEVER ON QUICK CAST!) */}
      {pendingChantSpell && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/80 backdrop-blur-md"
            onClick={() => setPendingChantSpell(null)}
          />
          <div className="modal-content relative w-full max-w-lg rounded-2xl p-6 text-center z-10 max-h-[90vh] overflow-y-auto">
            <h4 className="text-xs uppercase tracking-widest text-magic-gold font-cinzel mb-1">
              Chanting Phase (Full Immersion)
            </h4>
            <h3 className="font-cinzel text-2xl font-bold text-white mb-3">
              {pendingChantSpell.en}
            </h3>

            {/* JP Chant Box */}
            <div className="bg-black/60 border border-blue-500/30 rounded-xl p-3 text-left mb-2">
              <span className="text-[10px] text-blue-400 uppercase font-cinzel block mb-1">🇯🇵 Japanese Chant:</span>
              <div className="font-jp text-base text-white font-bold leading-relaxed mb-1">
                「{pendingChantSpell.jp}」
              </div>
              <div className="text-xs text-magic-gold-light italic">
                {pendingChantSpell.romaji}
              </div>
            </div>

            {/* TH Chant Box */}
            <div className="bg-black/60 border border-amber-500/30 rounded-xl p-3 text-left mb-4">
              <span className="text-[10px] text-amber-400 uppercase font-cinzel block mb-1">🇹🇭 Thai Chant:</span>
              <div className="text-xs text-gray-200 font-light italic leading-relaxed whitespace-pre-line">
                "{pendingChantSpell.th}"
              </div>
            </div>

            {/* Lang switcher for Chant Speech */}
            <div className="flex justify-center items-center gap-2 mb-3">
              <span className="text-[11px] text-gray-400 font-cinzel uppercase">Voice Lang:</span>
              <button
                type="button"
                onClick={() => setChantLang('ja-JP')}
                className={`px-2.5 py-0.5 rounded text-xs cursor-pointer font-cinzel ${
                  chantLang === 'ja-JP' ? 'bg-blue-600/40 text-blue-200 border border-blue-400' : 'bg-white/5 text-gray-400'
                }`}
              >
                🇯🇵 JP
              </button>
              <button
                type="button"
                onClick={() => setChantLang('th-TH')}
                className={`px-2.5 py-0.5 rounded text-xs cursor-pointer font-cinzel ${
                  chantLang === 'th-TH' ? 'bg-amber-600/40 text-amber-200 border border-amber-400' : 'bg-white/5 text-gray-400'
                }`}
              >
                🇹🇭 TH
              </button>
            </div>

            {/* Mic and Voice Buttons */}
            <div className="flex justify-center items-center gap-3 mb-3">
              <button
                type="button"
                onClick={toggleChantSpeech}
                className={`w-14 h-14 rounded-full bg-white/5 border-2 border-magic-gold text-magic-gold flex items-center justify-center hover:bg-magic-gold/20 transition-all cursor-pointer ${
                  isChantRecording ? 'recording-pulse' : ''
                }`}
                title="Chant with microphone in selected language"
              >
                <Mic className="w-6 h-6" />
              </button>
              <button
                type="button"
                onClick={() => {
                  if (!('speechSynthesis' in window)) return;
                  const text = chantLang === 'th-TH' ? pendingChantSpell.th : pendingChantSpell.jp;
                  const u = new SpeechSynthesisUtterance(text);
                  u.lang = chantLang;
                  window.speechSynthesis.speak(u);
                }}
                className="w-10 h-10 rounded-full bg-white/5 border border-white/20 text-gray-300 hover:text-white flex items-center justify-center cursor-pointer"
                title="Hear incantation audio"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            </div>

            <div className="text-xs text-gray-400 mb-3 min-h-[20px]">
              {chantTranscript || 'กดไมค์แล้วท่องบทสวด (JP หรือ TH) หรือพิมพ์คำร่ายด้านล่าง'}
            </div>

            {/* Typing input inside modal */}
            <form onSubmit={handleChantTypeCast} className="mb-4 flex gap-2">
              <input
                type="text"
                value={chantTypedText}
                onChange={(e) => setChantTypedText(e.target.value)}
                placeholder="พิมพ์คำร่าย (JP หรือ TH)..."
                className="flex-1 bg-black/60 border border-white/15 rounded-lg px-3 py-1.5 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-magic-gold font-prompt"
              />
              <button
                type="submit"
                className="px-3 py-1.5 bg-magic-gold/20 hover:bg-magic-gold/30 border border-magic-gold text-magic-gold text-xs font-cinzel rounded-lg cursor-pointer"
              >
                Cast By Typing
              </button>
            </form>

            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setPendingChantSpell(null)}
                className="w-1/3 py-2 bg-white/5 hover:bg-white/10 text-xs text-gray-400 font-cinzel uppercase rounded-lg border border-white/10 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => executeCast(pendingChantSpell, 'Chanted (Fast Cast skipped mic) 📜')}
                className="w-2/3 py-2 bg-gradient-to-r from-magic-gold to-yellow-500 text-magic-dark font-cinzel font-bold text-xs uppercase rounded-lg hover:scale-[1.02] transition-transform cursor-pointer shadow-[0_0_15px_rgba(197,160,89,0.3)] flex items-center justify-center gap-1.5"
              >
                <Sparkles className="w-3.5 h-3.5" /> Fast Cast (Skip Mic)
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};
