import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Spell } from '../types';
import { evaluateChant, EvaluationResult } from '../utils/chantEvaluator';
import {
  GraduationCap,
  Zap,
  Mic,
  Volume2,
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Keyboard,
  Globe,
  Sparkles,
} from 'lucide-react';

interface TrainingViewProps {
  spells: Spell[];
  initialSpell?: Spell | null;
}

export const TrainingView: React.FC<TrainingViewProps> = ({ spells, initialSpell }) => {
  const [targetElement, setTargetElement] = useState<string>('Water');
  const [tier1Count, setTier1Count] = useState<number>(1);
  const [tier2Count, setTier2Count] = useState<number>(1);

  const [queue, setQueue] = useState<Spell[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);

  // Mode: speak or type
  const [inputMode, setInputMode] = useState<'speak' | 'type'>('speak');
  const [speechLang, setSpeechLang] = useState<'ja-JP' | 'th-TH'>('ja-JP');

  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [transcript, setTranscript] = useState<string>('');
  const [typedInput, setTypedInput] = useState<string>('');
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recognitionRef = useRef<any>(null);
  const accumulatedRef = useRef<string>('');

  // If an initial spell was passed from the Grimoire modal, load it into queue!
  useEffect(() => {
    if (initialSpell) {
      setQueue([initialSpell]);
      setCurrentIndex(0);
      setTranscript('');
      setTypedInput('');
      setEvaluation(null);
    }
  }, [initialSpell]);

  const currentSpell = queue[currentIndex] || null;

  const handleEvaluate = useCallback((text: string, spell: Spell) => {
    const result = evaluateChant(text, spell);
    setEvaluation(result);
  }, []);

  const handleGenerateQueue = () => {
    // Only magic spells for Chanting Training (Sword techniques do not have chants)
    let pool = spells.filter((s) => s.element !== 'Sword' && !s.sword_school);
    if (targetElement !== 'All') {
      pool = pool.filter((s) => s.element.toLowerCase() === targetElement.toLowerCase());
    }

    const t1 = [...pool.filter((s) => s.tier === 'tier1')].sort(() => Math.random() - 0.5).slice(0, tier1Count);
    const t2 = [...pool.filter((s) => s.tier === 'tier2')].sort(() => Math.random() - 0.5).slice(0, tier2Count);

    const newQueue = [...t1, ...t2];
    if (newQueue.length === 0) {
      alert('No spells match this element and tier count combination.');
      return;
    }

    setQueue(newQueue);
    setCurrentIndex(0);
    setTranscript('');
    setTypedInput('');
    setEvaluation(null);
  };

  const playVoice = (text: string, lang: 'ja-JP' | 'th-TH') => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported in this browser.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  const toggleRecording = () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setInputMode('type');
      return;
    }

    if (isRecording) {
      setIsRecording(false);
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (accumulatedRef.current.trim() && currentSpell) {
        handleEvaluate(accumulatedRef.current, currentSpell);
      }
    } else {
      accumulatedRef.current = '';
      setTranscript('');
      setEvaluation(null);

      try {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = speechLang;

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        recognition.onresult = (e: any) => {
          let interim = '';
          for (let i = e.resultIndex; i < e.results.length; ++i) {
            interim += e.results[i][0].transcript;
            if (e.results[i].isFinal) {
              accumulatedRef.current += ' ' + e.results[i][0].transcript;
            }
          }
          const liveHeard = (accumulatedRef.current + ' ' + interim).trim();
          setTranscript(liveHeard);

          if (currentSpell) {
            const jpTrigger = (currentSpell.jp_name || currentSpell.en).toLowerCase();
            const thTrigger = currentSpell.name.split('(')[0].trim().toLowerCase();
            const cleanLive = liveHeard.toLowerCase();

            if (
              (cleanLive.includes(jpTrigger) && cleanLive.length >= 8) ||
              (cleanLive.includes(thTrigger) && cleanLive.length >= 8)
            ) {
              setTimeout(() => {
                recognition.stop();
                setIsRecording(false);
                handleEvaluate(liveHeard, currentSpell);
              }, 600);
            }
          }
        };

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        recognition.onerror = (err: any) => {
          setIsRecording(false);
          setTranscript(`Notice: ${err.error || 'Mic error'}. สามารถพิมพ์บทสวดเพื่อตรวจสอบได้เช่นกัน`);
        };

        recognition.onend = () => {
          setIsRecording(false);
        };

        recognition.start();
        recognitionRef.current = recognition;
        setIsRecording(true);
      } catch (err) {
        console.warn('Speech recognition error:', err);
        setInputMode('type');
      }
    }
  };

  const handleTypeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!typedInput.trim() || !currentSpell) return;
    setTranscript(typedInput);
    handleEvaluate(typedInput, currentSpell);
  };

  return (
    <section>
      {/* Training Queue Generator Configuration */}
      <div className="bg-gradient-to-b from-[#111a24] to-[#0d121c] border-2 border-magic-gold/40 rounded-3xl p-6 md:p-8 backdrop-blur-md max-w-4xl mx-auto mb-10 shadow-2xl">
        <div className="text-center mb-6">
          <h3 className="font-cinzel text-2xl font-bold text-white mb-2 text-glow flex items-center justify-center gap-2">
            <GraduationCap className="w-6 h-6 text-magic-gold" />
            Chanting Academy (ฝึกร่ายเวท JP / TH)
          </h3>
          <p className="text-gray-400 text-sm">
            รองรับทั้งภาษาญี่ปุ่นและภาษาไทย ทั้งแบบพูดออกเสียง (Microphone) และพิมพ์ข้อความ (Text Input)
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-magic-dark/60 border border-magic-gold/20 p-4 rounded-xl">
            <label className="block text-xs uppercase text-gray-400 font-cinzel mb-2">
              Target Element (ธาตุเป้าหมาย):
            </label>
            <select
              value={targetElement}
              onChange={(e) => setTargetElement(e.target.value)}
              className="w-full py-2 px-3 rounded-lg text-sm"
            >
              <option value="All">All Elements (全属性 - ทุกธาตุเวทมนตร์)</option>
              <option value="Water">Water / Ice (น้ำ / น้ำแข็ง)</option>
              <option value="Fire">Fire (ไฟ)</option>
              <option value="Earth">Earth (ดิน)</option>
              <option value="Wind">Wind (ลม)</option>
              <option value="Healing">Healing (การรักษา / ศักดิ์สิทธิ์)</option>
              <option value="Dragon">Dragon Summon / Ancient (มังกรโบราณ)</option>
            </select>
          </div>

          <div className="bg-magic-dark/60 border border-magic-gold/20 p-4 rounded-xl">
            <label className="block text-xs uppercase text-gray-400 font-cinzel mb-2">
              Tier 1: Low-Mid (ระดับต้น - กลาง)
            </label>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-300">Count:</span>
              <input
                type="number"
                min="0"
                max="5"
                value={tier1Count}
                onChange={(e) => setTier1Count(Math.max(0, parseInt(e.target.value) || 0))}
                className="w-20 bg-magic-dark border border-magic-gold/30 rounded py-1 px-2 text-center text-white text-sm"
              />
            </div>
          </div>

          <div className="bg-magic-dark/60 border border-magic-gold/20 p-4 rounded-xl">
            <label className="block text-xs uppercase text-gray-400 font-cinzel mb-2">
              Tier 2: High-God (ระดับสูง - ศักดิ์สิทธิ์ - ราชา)
            </label>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-300">Count:</span>
              <input
                type="number"
                min="0"
                max="5"
                value={tier2Count}
                onChange={(e) => setTier2Count(Math.max(0, parseInt(e.target.value) || 0))}
                className="w-20 bg-magic-dark border border-magic-gold/30 rounded py-1 px-2 text-center text-white text-sm"
              />
            </div>
          </div>
        </div>

        <div className="text-center">
          <button
            type="button"
            onClick={handleGenerateQueue}
            className="bg-gradient-to-r from-magic-gold via-yellow-200 to-magic-gold text-magic-dark font-cinzel font-bold py-3 px-8 rounded-full text-sm uppercase tracking-wider hover:scale-105 transition-transform shadow-[0_0_20px_rgba(197,160,89,0.4)] cursor-pointer inline-flex items-center gap-2"
          >
            <Zap className="w-4 h-4 fill-current" />
            Generate Training Queue
          </button>
        </div>
      </div>

      {/* Training Stage Box */}
      {currentSpell && (
        <div className="bg-gradient-to-b from-[#111a24] to-[#151020] border-2 border-magic-gold rounded-3xl p-6 md:p-10 text-center max-w-4xl mx-auto shadow-2xl relative mb-12">
          {/* Header & Badges */}
          <div className="flex flex-wrap items-center justify-center gap-2 mb-6">
            <div className="inline-flex items-center gap-2 bg-black/50 px-4 py-1.5 rounded-full border border-magic-gold/30 text-xs text-gray-300 font-cinzel shadow-[0_0_15px_rgba(197,160,89,0.15)]">
              <Globe className="w-3.5 h-3.5 text-magic-gold" />
              Supported: <span className="text-magic-gold font-semibold">Japanese (日本語) & Thai (ไทย)</span>
            </div>
            <div className="inline-flex items-center gap-2 bg-black/50 px-4 py-1.5 rounded-full border border-magic-gold/30 text-xs text-gray-300 font-cinzel shadow-[0_0_15px_rgba(197,160,89,0.15)]">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              Mode: <span className="text-cyan-300 font-semibold">Speech 🎙️ + Typing ⌨️</span>
            </div>
          </div>

          <div className="font-cinzel text-magic-gold text-xs tracking-widest uppercase mb-1">
            STAGE {currentIndex + 1} / {queue.length} ({currentSpell.rank})
          </div>
          <h3 className="font-cinzel text-2xl md:text-3xl font-bold text-white mb-4 text-glow">
            {currentSpell.en}{' '}
            <span className="text-lg md:text-xl text-magic-gold-light font-normal block md:inline font-prompt">
              ({currentSpell.name.split('(')[0].trim()})
            </span>
          </h3>

          {/* Active Chant Box */}
          <div className="bg-black/60 border border-magic-gold/30 rounded-2xl p-5 md:p-7 mb-6 text-left">
            <div className="text-xs uppercase text-blue-400 font-cinzel mb-2 flex items-center justify-between">
              <span>🇯🇵 1. Japanese Incantation (คำร่ายภาษาญี่ปุ่น):</span>
              <button
                type="button"
                onClick={() => playVoice(currentSpell.jp, 'ja-JP')}
                className="text-magic-gold hover:text-white text-[11px] font-cinzel uppercase flex items-center gap-1 cursor-pointer"
              >
                <Volume2 className="w-3.5 h-3.5" /> JP Voice
              </button>
            </div>
            <div className="font-jp text-lg md:text-xl text-white font-bold leading-relaxed mb-3">
              「{currentSpell.jp}」
            </div>

            <div className="text-xs uppercase text-magic-gold font-cinzel mb-1">
              🔤 2. Romaji (คำอ่านโรมาจิ):
            </div>
            <div className="text-sm md:text-base text-magic-gold-light italic leading-relaxed mb-3">
              {currentSpell.romaji}
            </div>

            <div className="h-px bg-white/10 my-3" />

            <div className="text-xs uppercase text-amber-400 font-cinzel mb-2 flex items-center justify-between">
              <span>🇹🇭 3. Thai Incantation (บทร่ายและความหมายภาษาไทย):</span>
              <button
                type="button"
                onClick={() => playVoice(currentSpell.th, 'th-TH')}
                className="text-amber-400 hover:text-white text-[11px] font-cinzel uppercase flex items-center gap-1 cursor-pointer"
              >
                <Volume2 className="w-3.5 h-3.5" /> TH Voice
              </button>
            </div>
            <div className="text-sm md:text-base text-gray-200 font-light leading-relaxed whitespace-pre-line italic">
              "{currentSpell.th}"
            </div>
          </div>

          {/* Input Method Switcher (Speak 🎙️ vs Type ⌨️) */}
          <div className="flex justify-center items-center gap-2 mb-6">
            <button
              type="button"
              onClick={() => setInputMode('speak')}
              className={`px-5 py-2 rounded-full text-xs font-cinzel uppercase tracking-wider font-semibold transition-all flex items-center gap-1.5 cursor-pointer ${
                inputMode === 'speak'
                  ? 'bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]'
                  : 'bg-magic-blue/60 text-gray-300 hover:text-white border border-magic-gold/20'
              }`}
            >
              <Mic className="w-3.5 h-3.5" /> Speak Chant (พูดออกเสียง)
            </button>
            <button
              type="button"
              onClick={() => setInputMode('type')}
              className={`px-5 py-2 rounded-full text-xs font-cinzel uppercase tracking-wider font-semibold transition-all flex items-center gap-1.5 cursor-pointer ${
                inputMode === 'type'
                  ? 'bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]'
                  : 'bg-magic-blue/60 text-gray-300 hover:text-white border border-magic-gold/20'
              }`}
            >
              <Keyboard className="w-3.5 h-3.5" /> Type Chant (พิมพ์บทร่าย)
            </button>
          </div>

          {/* MODE 1: SPEAKING */}
          {inputMode === 'speak' && (
            <div className="mb-6 space-y-4">
              {/* Language Selector for Speech */}
              <div className="flex justify-center items-center gap-2">
                <span className="text-xs text-gray-400 font-cinzel uppercase">Voice Recognition Lang:</span>
                <button
                  type="button"
                  onClick={() => setSpeechLang('ja-JP')}
                  className={`px-3 py-1 rounded-lg text-xs font-cinzel uppercase transition-all cursor-pointer ${
                    speechLang === 'ja-JP'
                      ? 'bg-blue-600/40 text-blue-200 border border-blue-400 font-bold'
                      : 'bg-white/5 text-gray-400 hover:text-white border border-white/10'
                  }`}
                >
                  🇯🇵 Japanese (ja-JP)
                </button>
                <button
                  type="button"
                  onClick={() => setSpeechLang('th-TH')}
                  className={`px-3 py-1 rounded-lg text-xs font-cinzel uppercase transition-all cursor-pointer ${
                    speechLang === 'th-TH'
                      ? 'bg-amber-600/40 text-amber-200 border border-amber-400 font-bold'
                      : 'bg-white/5 text-gray-400 hover:text-white border border-white/10'
                  }`}
                >
                  🇹🇭 Thai (th-TH)
                </button>
              </div>

              {/* Mic and Voice Buttons */}
              <div className="flex justify-center items-center gap-4">
                <button
                  type="button"
                  onClick={toggleRecording}
                  className={`w-16 h-16 rounded-full bg-white/5 border-2 border-magic-gold text-magic-gold text-2xl flex items-center justify-center hover:bg-magic-gold/20 hover:scale-105 transition-all shadow-[0_0_15px_rgba(197,160,89,0.2)] cursor-pointer ${
                    isRecording ? 'recording-pulse' : ''
                  }`}
                  title={isRecording ? 'Click to finish chant' : 'Click to start chant recitation'}
                >
                  <Mic className="w-6 h-6" />
                </button>

                <button
                  type="button"
                  onClick={() => playVoice(speechLang === 'th-TH' ? currentSpell.th : currentSpell.jp, speechLang)}
                  className="px-5 py-3 rounded-xl bg-magic-blue/80 border border-magic-gold/40 text-gray-200 hover:text-white hover:border-magic-gold text-xs font-cinzel uppercase tracking-wider flex items-center gap-2 cursor-pointer transition-colors"
                >
                  <Volume2 className="w-4 h-4 text-magic-gold" />
                  Listen Master Chant
                </button>
              </div>

              {/* Speech Transcript Box */}
              <div className="bg-black/40 border border-dashed border-gray-600 rounded-xl p-4 max-w-2xl mx-auto text-xs md:text-sm text-gray-400 min-h-[50px] flex items-center justify-center">
                {isRecording ? (
                  <span className="text-magic-gold animate-pulse">
                    🎙️ Listening ({speechLang === 'th-TH' ? 'ภาษาไทย' : 'Japanese'})... Recite now, and click mic when finished!
                  </span>
                ) : transcript ? (
                  <span className="text-white">Heard: "{transcript}"</span>
                ) : (
                  <span>กดปุ่มไมโครโฟนแล้วท่องบทสวดเต็มบท (ทั้งภาษาญี่ปุ่น หรือภาษาไทย)...</span>
                )}
              </div>
            </div>
          )}

          {/* MODE 2: TYPING */}
          {inputMode === 'type' && (
            <div className="mb-6 max-w-2xl mx-auto">
              <form onSubmit={handleTypeSubmit} className="space-y-3">
                <textarea
                  value={typedInput}
                  onChange={(e) => setTypedInput(e.target.value)}
                  placeholder="พิมพ์บทร่ายเวทมนตร์ (ภาษาญี่ปุ่น, โรมะจิ, หรือคำร่ายภาษาไทย)..."
                  rows={3}
                  className="w-full bg-black/60 border border-magic-gold/40 rounded-xl p-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-magic-gold font-prompt"
                />

                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex gap-2">
                    <button
                      type="button"
                      onClick={() => setTypedInput(currentSpell.jp)}
                      className="px-2.5 py-1 bg-white/5 hover:bg-white/10 text-[11px] text-blue-300 rounded border border-blue-400/30 font-cinzel cursor-pointer"
                    >
                      Paste JP Chant
                    </button>
                    <button
                      type="button"
                      onClick={() => setTypedInput(currentSpell.th)}
                      className="px-2.5 py-1 bg-white/5 hover:bg-white/10 text-[11px] text-amber-300 rounded border border-amber-400/30 font-cinzel cursor-pointer"
                    >
                      Paste Thai Chant
                    </button>
                  </div>

                  <button
                    type="submit"
                    className="px-6 py-2 bg-gradient-to-r from-magic-gold to-yellow-500 text-magic-dark font-cinzel font-bold text-xs uppercase rounded-lg hover:scale-105 transition-transform shadow-[0_0_15px_rgba(197,160,89,0.3)] cursor-pointer"
                  >
                    Evaluate Chant (ตรวจคำร่าย)
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Result Badge */}
          {evaluation && (
            <div className="mb-6">
              {evaluation.rank === 'S' && (
                <div className="inline-block px-5 py-2.5 rounded-full bg-green-500/20 border-2 border-green-500 text-green-300 font-cinzel text-sm shadow-[0_0_20px_rgba(16,185,129,0.4)]">
                  <CheckCircle2 className="w-4 h-4 inline-block mr-2 text-green-400" />
                  {evaluation.message}
                </div>
              )}
              {evaluation.rank === 'A' && (
                <div className="inline-block px-5 py-2.5 rounded-full bg-yellow-500/20 border border-yellow-500 text-yellow-300 font-cinzel text-sm">
                  <AlertTriangle className="w-4 h-4 inline-block mr-2 text-yellow-400" />
                  {evaluation.message}
                </div>
              )}
              {evaluation.rank === 'B' && (
                <div className="inline-block px-4 py-2 rounded-full bg-red-500/20 border border-red-500 text-red-300 font-cinzel text-sm">
                  <XCircle className="w-4 h-4 inline-block mr-2 text-red-400" />
                  {evaluation.message}
                </div>
              )}
            </div>
          )}

          {/* Navigation between queue */}
          <div className="flex justify-center gap-4">
            <button
              type="button"
              disabled={currentIndex === 0}
              onClick={() => {
                setCurrentIndex((prev) => Math.max(0, prev - 1));
                setTranscript('');
                setTypedInput('');
                setEvaluation(null);
              }}
              className="px-5 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 text-xs font-cinzel uppercase tracking-wider border border-white/10 disabled:opacity-30 disabled:pointer-events-none cursor-pointer flex items-center gap-1"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Prev
            </button>
            <button
              type="button"
              disabled={currentIndex >= queue.length - 1}
              onClick={() => {
                setCurrentIndex((prev) => Math.min(queue.length - 1, prev + 1));
                setTranscript('');
                setTypedInput('');
                setEvaluation(null);
              }}
              className="px-5 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 text-xs font-cinzel uppercase tracking-wider border border-white/10 disabled:opacity-30 disabled:pointer-events-none cursor-pointer flex items-center gap-1"
            >
              Next <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </section>
  );
};
