import json

with open('data.json', 'r', encoding='utf-8') as f:
    spells = json.load(f)

# Build HTML template based on firstOne.html's gorgeous card UI + modal + Training + Battle
html = '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mushoku Tensei: Magic Chants & Combat Grimoire</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Noto+Serif+JP:wght@400;600;700;900&family=Prompt:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        'cinzel': ['Cinzel', 'serif'],
                        'prompt': ['Prompt', 'sans-serif'],
                        'jp': ['Noto Serif JP', 'serif'],
                    },
                    colors: {
                        'magic-dark': '#0b0c10',
                        'magic-blue': '#1f2833',
                        'magic-gold': '#c5a059',
                        'magic-gold-light': '#e8d399',
                        'magic-purple': '#4a2545',
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #0b0c10;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(74, 37, 69, 0.4) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(20, 40, 80, 0.5) 0%, transparent 50%);
            background-attachment: fixed;
            color: #e0e0e0;
        }

        /* Glassmorphism spell card styling matching firstOne.html */
        .spell-card {
            background: rgba(31, 40, 51, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(197, 160, 89, 0.2);
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
        }

        .spell-card:hover {
            transform: translateY(-5px) scale(1.02);
            border-color: rgba(197, 160, 89, 0.8);
            box-shadow: 0 10px 30px -10px rgba(197, 160, 89, 0.5), inset 0 0 20px rgba(197, 160, 89, 0.1);
            background: rgba(31, 40, 51, 0.85);
        }

        .spell-card::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.05), transparent);
            transform: skewX(-25deg);
            transition: 0.5s;
        }
        .spell-card:hover::before {
            left: 200%;
        }

        /* Modal styling */
        #spell-modal, #training-modal {
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }
        #spell-modal.hidden, #training-modal.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        #spell-modal:not(.hidden), #training-modal:not(.hidden) {
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
        }
        
        .modal-content {
            transform: scale(0.95) translateY(20px);
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            background: linear-gradient(135deg, #111a22 0%, #1a1025 100%);
            border: 2px solid #c5a059;
            box-shadow: 0 0 50px rgba(197, 160, 89, 0.25), inset 0 0 30px rgba(197, 160, 89, 0.08);
        }
        
        #spell-modal:not(.hidden) .modal-content, #training-modal:not(.hidden) .modal-content {
            transform: scale(1) translateY(0);
        }

        .text-glow {
            text-shadow: 0 0 10px rgba(197, 160, 89, 0.6);
        }

        .grid-fade-out {
            opacity: 0;
            transform: translateY(10px);
            transition: opacity 0.25s ease, transform 0.25s ease;
        }
        .grid-fade-in {
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.25s ease, transform 0.25s ease;
        }
        
        select {
            background-color: rgba(31, 40, 51, 0.8);
            border: 1px solid rgba(197, 160, 89, 0.4);
            color: #e8d399;
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23c5a059' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 1rem center;
            background-size: 1em;
        }
        select:focus {
            outline: none;
            border-color: rgba(197, 160, 89, 0.9);
            box-shadow: 0 0 15px rgba(197, 160, 89, 0.3);
        }
        select option {
            background-color: #0b0c10;
            color: #e0e0e0;
        }

        /* Pulse mic animation */
        @keyframes micPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.08); }
            100% { transform: scale(1); }
        }
        .recording-pulse {
            animation: micPulse 1.2s infinite;
            background: #dc2626 !important;
            border-color: #f87171 !important;
            color: #fff !important;
            box-shadow: 0 0 30px rgba(239, 68, 68, 0.8) !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0b0c10; }
        ::-webkit-scrollbar-thumb { background: #c5a059; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #e8d399; }
    </style>
</head>
<body class="font-prompt min-h-screen relative overflow-x-hidden antialiased">

    <!-- Ambient Particles Canvas -->
    <canvas id="particle-canvas" class="fixed inset-0 pointer-events-none z-0 opacity-40"></canvas>

    <div class="container mx-auto px-4 py-8 relative z-10 max-w-7xl">
        
        <!-- Header -->
        <header class="text-center mb-10">
            <h2 class="font-cinzel text-magic-gold text-sm md:text-base tracking-widest uppercase mb-2 opacity-80">Grimoire of Six-Faced World</h2>
            <h1 class="font-cinzel text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-magic-gold via-yellow-200 to-magic-gold mb-4 text-glow">
                Mushoku Tensei<br/><span class="text-2xl md:text-4xl mt-1 block text-white/90 font-normal">Magic Chants Archive</span>
            </h1>
            <p class="text-gray-400 max-w-2xl mx-auto font-light text-sm md:text-base leading-relaxed">
                คลังบทสวดและคำร่ายเวทมนตร์ฉบับสมบูรณ์ คลิกที่การ์ดเพื่อดูรายละเอียดบทสวดเต็ม หรือเข้าสู่โหมดฝึกท่องและเกมประลองเวทมนตร์
            </p>
            <div class="h-px w-32 bg-gradient-to-r from-transparent via-magic-gold to-transparent mx-auto mt-6 opacity-50"></div>

            <!-- Navigation Mode Switcher -->
            <div class="flex justify-center items-center gap-3 mt-8 flex-wrap">
                <button onclick="switchTab('grimoire')" id="tab-btn-grimoire" class="px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]">
                    <i class="fa-solid fa-book-sparkles mr-2"></i> Grimoire Archive
                </button>
                <button onclick="switchTab('training')" id="tab-btn-training" class="px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold">
                    <i class="fa-solid fa-microphone-lines mr-2"></i> Chanting Training (JP/Romaji)
                </button>
                <button onclick="switchTab('battle')" id="tab-btn-battle" class="px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold">
                    <i class="fa-solid fa-dragon mr-2"></i> Spell Battle RPG
                </button>
            </div>
        </header>

        <!-- ======================================================== -->
        <!-- VIEW 1: GRIMOIRE CARDS (Exact firstOne.html design) -->
        <!-- ======================================================== -->
        <section id="view-grimoire">
            <!-- Controls (Search, Sort & Filter) -->
            <div class="flex flex-col md:flex-row justify-between items-center mb-8 gap-4 bg-magic-blue/40 p-4 rounded-xl border border-magic-gold/20 backdrop-blur-sm z-20 relative shadow-[0_4px_20px_rgba(0,0,0,0.5)]">
                <!-- Search Box -->
                <div class="relative w-full md:w-72">
                    <input type="text" id="search-input" oninput="applyFiltersAndSort()" placeholder="ค้นหาเวทมนตร์ (Search)..." class="w-full bg-magic-dark/80 border border-magic-gold/30 rounded-lg py-2 pl-9 pr-4 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-magic-gold focus:ring-1 focus:ring-magic-gold">
                    <i class="fa-solid fa-magnifying-glass absolute left-3 top-3 text-gray-400 text-xs"></i>
                </div>

                <div class="flex flex-wrap md:flex-nowrap gap-4 w-full md:w-auto">
                    <div class="flex items-center gap-3 w-full md:w-auto">
                        <label for="sort-select" class="text-gray-400 font-cinzel text-xs uppercase tracking-wider whitespace-nowrap">Sort By:</label>
                        <select id="sort-select" onchange="applyFiltersAndSort()" class="w-full md:w-56 py-2 pl-4 pr-10 rounded-lg cursor-pointer font-prompt text-sm transition-all">
                            <option value="element" selected>เรียงตามธาตุและขั้น (Element & Tier)</option>
                            <option value="level">เรียงตามลำดับขั้น (Tier / Level)</option>
                            <option value="id">ลำดับตาม ID ดั้งเดิม (Original ID)</option>
                        </select>
                    </div>
                    
                    <div class="flex items-center gap-3 w-full md:w-auto">
                        <label for="filter-select" class="text-gray-400 font-cinzel text-xs uppercase tracking-wider whitespace-nowrap">Filter:</label>
                        <select id="filter-select" onchange="applyFiltersAndSort()" class="w-full md:w-44 py-2 pl-4 pr-10 rounded-lg cursor-pointer font-prompt text-sm transition-all">
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

            <!-- Spell Grid -->
            <div id="spell-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 transition-all duration-300">
                <!-- Cards injected here via JavaScript -->
            </div>
        </section>

        <!-- ======================================================== -->
        <!-- VIEW 2: TRAINING MODE (JP + ROMAJI ONLY) -->
        <!-- ======================================================== -->
        <section id="view-training" class="hidden">
            <div class="bg-magic-blue/50 border border-magic-gold/40 rounded-2xl p-6 md:p-8 backdrop-blur-md max-w-4xl mx-auto shadow-2xl mb-8">
                <div class="text-center mb-6">
                    <span class="text-xs uppercase tracking-widest text-magic-gold font-cinzel">Chanting Academy</span>
                    <h2 class="font-cinzel text-2xl md:text-3xl font-bold text-white mt-1">Custom Incantation Practice</h2>
                    <p class="text-gray-400 text-xs md:text-sm mt-1">In training mode, only <strong>Japanese script and Romaji</strong> are displayed. Accent-tolerant speech recognition enabled!</p>
                </div>

                <!-- Config Options -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div class="bg-magic-dark/60 border border-magic-gold/20 p-4 rounded-xl">
                        <label class="block text-xs uppercase text-gray-400 font-cinzel mb-2">Target Element</label>
                        <select id="train-element-select" class="w-full py-2 px-3 rounded-lg text-sm">
                            <option value="All">All Elements (全属性)</option>
                            <option value="Water" selected>Water / Ice (水・氷)</option>
                            <option value="Fire">Fire (火)</option>
                            <option value="Earth">Earth (土)</option>
                            <option value="Healing">Healing (治癒)</option>
                            <option value="Dragon">Dragon Summon (龍神)</option>
                        </select>
                    </div>

                    <div class="bg-magic-dark/60 border border-magic-gold/20 p-4 rounded-xl">
                        <label class="block text-xs uppercase text-gray-400 font-cinzel mb-2">Tier 1: Low-Mid (初・中級)</label>
                        <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-300">Count:</span>
                            <input type="number" id="train-tier1-count" min="0" max="5" value="1" class="w-20 bg-magic-dark border border-magic-gold/30 rounded py-1 px-2 text-center text-white text-sm">
                        </div>
                    </div>

                    <div class="bg-magic-dark/60 border border-magic-gold/20 p-4 rounded-xl">
                        <label class="block text-xs uppercase text-gray-400 font-cinzel mb-2">Tier 2: High-God (上・聖・王・神級)</label>
                        <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-300">Count:</span>
                            <input type="number" id="train-tier2-count" min="0" max="5" value="1" class="w-20 bg-magic-dark border border-magic-gold/30 rounded py-1 px-2 text-center text-white text-sm">
                        </div>
                    </div>
                </div>

                <div class="text-center">
                    <button onclick="generateTrainingQueue()" class="bg-gradient-to-r from-magic-gold via-yellow-200 to-magic-gold text-magic-dark font-cinzel font-bold py-3 px-8 rounded-full text-sm uppercase tracking-wider hover:scale-105 transition-transform shadow-[0_0_20px_rgba(197,160,89,0.4)]">
                        <i class="fa-solid fa-bolt mr-2"></i> Generate Training Queue
                    </button>
                </div>
            </div>

            <!-- Training Stage Box -->
            <div id="training-stage-box" class="hidden bg-gradient-to-b from-[#111a24] to-[#151020] border-2 border-magic-gold rounded-3xl p-6 md:p-10 text-center max-w-4xl mx-auto shadow-2xl relative">
                <div id="train-counter" class="font-cinzel text-magic-gold text-xs tracking-widest uppercase mb-1">STAGE 1 / 2</div>
                <h3 id="train-spell-name" class="font-cinzel text-2xl md:text-3xl font-bold text-white mb-6 text-glow">Water Ball</h3>

                <div class="bg-black/60 border border-magic-gold/30 rounded-2xl p-6 md:p-8 mb-6 text-left">
                    <div class="text-xs uppercase text-gray-400 font-cinzel mb-2">Japanese Incantation:</div>
                    <div id="train-jp-text" class="font-jp text-xl md:text-2xl text-white font-bold leading-relaxed mb-4">
                        「汝の求める所に大いなる水の加護あらん、清涼なるせせらぎの流れを今ここに、ウォーターボール」
                    </div>
                    <div class="text-xs uppercase text-magic-gold font-cinzel mb-1">Romaji:</div>
                    <div id="train-romaji-text" class="text-base md:text-lg text-magic-gold-light italic leading-relaxed">
                        Nanji no motomeru tokoro ni oinaru mizu no kago aran, seiryo naru seseragi no nagare o ima koko ni, Wota Boru
                    </div>
                </div>

                <!-- Mic and Pronounce Controls -->
                <div class="flex justify-center items-center gap-4 mb-6">
                    <button id="train-mic-btn" onclick="toggleTrainingSpeech()" class="w-16 h-16 rounded-full bg-white/5 border-2 border-magic-gold text-magic-gold text-2xl flex items-center justify-center hover:bg-magic-gold/20 hover:scale-105 transition-all shadow-[0_0_15px_rgba(197,160,89,0.2)]">
                        <i class="fa-solid fa-microphone"></i>
                    </button>
                    <button onclick="playCurrentTrainingAudio()" class="px-5 py-3 rounded-xl bg-magic-blue/80 border border-magic-gold/40 text-gray-200 hover:text-white hover:border-magic-gold text-xs font-cinzel uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-volume-high text-magic-gold"></i> Master Voice
                    </button>
                </div>

                <!-- Speech Transcript Box -->
                <div id="train-transcript-box" class="bg-black/40 border border-dashed border-gray-600 rounded-xl p-4 max-w-2xl mx-auto mb-6 text-sm text-gray-400 min-h-[50px] flex items-center justify-center">
                    <span>Press microphone button and chant in Japanese or Romaji...</span>
                </div>

                <div id="train-result-badge" class="mb-6"></div>

                <!-- Navigation between queue -->
                <div class="flex justify-center gap-4">
                    <button onclick="navigateTraining(-1)" id="train-prev-btn" class="px-5 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 text-xs font-cinzel uppercase tracking-wider border border-white/10">
                        <i class="fa-solid fa-arrow-left mr-1"></i> Prev
                    </button>
                    <button onclick="navigateTraining(1)" id="train-next-btn" class="px-5 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 text-xs font-cinzel uppercase tracking-wider border border-white/10">
                        Next <i class="fa-solid fa-arrow-right ml-1"></i>
                    </button>
                </div>
            </div>
        </section>

        <!-- ======================================================== -->
        <!-- VIEW 3: BALANCED SPELL BATTLE RPG -->
        <!-- ======================================================== -->
        <section id="view-battle" class="hidden">
            <div class="bg-gradient-to-b from-[#111a24] to-[#0d121c] border-2 border-magic-gold/40 rounded-3xl p-6 md:p-8 backdrop-blur-md max-w-5xl mx-auto shadow-2xl">
                <!-- Battle Top Header -->
                <div class="flex flex-col sm:flex-row justify-between items-center pb-4 mb-6 border-b border-magic-gold/20 gap-3">
                    <div>
                        <span class="text-xs uppercase tracking-widest text-magic-gold font-cinzel">Turn-Based Arena</span>
                        <h2 class="font-cinzel text-2xl font-bold text-white">Labyrinth Battle Simulator</h2>
                    </div>
                    <div class="flex items-center gap-3">
                        <label class="text-xs text-gray-400 font-cinzel uppercase">Enemy:</label>
                        <select id="battle-enemy-select" onchange="initBattle()" class="py-1.5 px-3 rounded-lg text-xs">
                            <option value="crawler" selected>Iron Crawler (Weak: Ice/Lightning)</option>
                            <option value="treant">Forest Treant (Weak: Fire)</option>
                            <option value="salamander">Magma Salamander (Weak: Water)</option>
                            <option value="wyvern">Red Wyvern (Weak: Cumulonimbus/Dragon)</option>
                        </select>
                        <button onclick="initBattle()" class="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-magic-gold/30 text-xs text-magic-gold">
                            <i class="fa-solid fa-rotate-right"></i>
                        </button>
                    </div>
                </div>

                <!-- Combatants Status Row -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <!-- Player -->
                    <div class="bg-black/40 border border-magic-gold/20 rounded-xl p-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="font-cinzel text-white font-bold"><i class="fa-solid fa-hat-wizard text-blue-400 mr-2"></i>Rudeus (Mage)</span>
                            <span class="text-xs px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-cinzel">Ready</span>
                        </div>
                        <div class="flex justify-between text-xs text-gray-400 mb-1">
                            <span>HP: <strong id="player-hp-text" class="text-white">500 / 500</strong></span>
                        </div>
                        <div class="w-full bg-black/60 rounded-full h-3 border border-gray-700 overflow-hidden mb-3">
                            <div id="player-hp-bar" class="bg-gradient-to-r from-red-500 to-green-500 h-full rounded-full transition-all duration-300" style="width: 100%;"></div>
                        </div>
                        <div class="flex justify-between text-xs text-gray-400 mb-1">
                            <span>MP: <strong id="player-mp-text" class="text-blue-300">350 / 350</strong></span>
                        </div>
                        <div class="w-full bg-black/60 rounded-full h-3 border border-gray-700 overflow-hidden">
                            <div id="player-mp-bar" class="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full transition-all duration-300" style="width: 100%;"></div>
                        </div>
                    </div>

                    <!-- Enemy -->
                    <div class="bg-black/40 border border-magic-gold/20 rounded-xl p-4">
                        <div class="flex justify-between items-center mb-2">
                            <span id="enemy-name-text" class="font-cinzel text-white font-bold"><i class="fa-solid fa-bug text-red-400 mr-2"></i>Iron Crawler</span>
                            <span id="enemy-type-badge" class="text-xs px-2 py-0.5 rounded bg-red-500/20 text-red-300 font-cinzel">Heavy Armor</span>
                        </div>
                        <div class="flex justify-between text-xs text-gray-400 mb-1">
                            <span>Enemy HP: <strong id="enemy-hp-text" class="text-white">750 / 750</strong></span>
                            <span id="enemy-weakness-text" class="text-xs text-cyan-400 font-medium">Weak: Ice / Thunder</span>
                        </div>
                        <div class="w-full bg-black/60 rounded-full h-3 border border-gray-700 overflow-hidden mb-3">
                            <div id="enemy-hp-bar" class="bg-gradient-to-r from-red-600 to-green-500 h-full rounded-full transition-all duration-300" style="width: 100%;"></div>
                        </div>
                        <div id="enemy-desc-text" class="text-xs text-gray-400">
                            Heavily armored labyrinth beast. Vulnerable to Water Splash + Freeze combos!
                        </div>
                    </div>
                </div>

                <!-- Combat Log -->
                <div id="battle-log-box" class="bg-black/60 border border-gray-800 rounded-xl p-4 text-xs md:text-sm text-gray-300 h-28 overflow-y-auto mb-6 leading-relaxed font-mono">
                    <div>[SYSTEM] Combat started. Select a spell below to chant, or speak any spell via Quick Cast!</div>
                </div>

                <!-- Spell Action Slots -->
                <div class="flex justify-between items-center mb-3">
                    <span class="text-xs uppercase font-cinzel text-magic-gold tracking-wider">Turn: <strong id="battle-turn-count" class="text-white">1</strong> • Available Spell Actions</span>
                    <button onclick="triggerQuickVoiceBattle()" class="px-3 py-1 bg-magic-gold/20 hover:bg-magic-gold/30 border border-magic-gold rounded-full text-xs text-magic-gold font-cinzel uppercase tracking-wider flex items-center gap-1.5 transition-all">
                        <i class="fa-solid fa-microphone"></i> Quick Voice Cast (Any Spell)
                    </button>
                </div>

                <div id="battle-slots-container" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
                    <!-- Populated dynamically via JS -->
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="mt-20 text-center text-gray-500 text-sm border-t border-white/10 pt-8 pb-4">
            <p class="font-cinzel">&copy; Six-Faced World Grimoire Archive • Mushoku Tensei Chants</p>
        </footer>
    </div>

    <!-- ======================================================== -->
    <!-- MODAL FOR SPELL DETAILS (Exact firstOne.html design) -->
    <!-- ======================================================== -->
    <div id="spell-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/80 backdrop-blur-md" onclick="closeModal()"></div>
        
        <!-- Modal Content -->
        <div class="modal-content relative w-full max-w-2xl rounded-2xl p-6 sm:p-8 text-left overflow-hidden z-10 max-h-[90vh] overflow-y-auto">
            <button onclick="closeModal()" class="absolute top-4 right-4 text-gray-400 hover:text-white bg-white/5 hover:bg-white/10 rounded-full p-2 transition-colors focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

            <div class="text-center mb-6 mt-2">
                <h3 id="modal-title" class="font-cinzel text-3xl sm:text-4xl font-bold text-magic-gold mb-1 text-glow"></h3>
                <h4 id="modal-romaji-title" class="text-lg text-magic-gold-light font-medium tracking-wide"></h4>
                <div id="modal-thai-title" class="text-sm text-gray-400 font-light mt-0.5"></div>
                <div class="inline-block px-3 py-1 bg-magic-gold/10 border border-magic-gold/30 rounded-full text-magic-gold-light text-xs mt-3 shadow-[0_0_10px_rgba(197,160,89,0.2)]">
                    <span id="modal-type"></span>
                </div>
            </div>

            <div class="space-y-4">
                <!-- 1. Japanese Chant -->
                <div class="bg-black/40 rounded-xl p-5 border-l-4 border-blue-500/70 relative overflow-hidden group">
                    <div class="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div class="flex justify-between items-center mb-2">
                        <h5 class="text-xs uppercase tracking-wider text-blue-400 font-cinzel font-semibold"><i class="fa-solid fa-torii-gate mr-1.5"></i> 1. Japanese (คำร่ายภาษาญี่ปุ่น)</h5>
                        <div class="flex gap-3">
                            <button id="modal-play-voice-btn" class="text-xs text-blue-400 hover:text-blue-300 font-cinzel"><i class="fa-solid fa-volume-high"></i> Voice</button>
                            <button id="modal-copy-jp-btn" class="text-xs text-blue-400 hover:text-blue-300 font-cinzel"><i class="fa-regular fa-copy"></i> Copy</button>
                        </div>
                    </div>
                    <p id="modal-jp-chant" class="font-jp text-base sm:text-lg text-gray-100 leading-relaxed font-bold">...</p>
                </div>

                <!-- 2. Romaji Chant -->
                <div class="bg-black/40 rounded-xl p-5 border-l-4 border-purple-500/70 relative overflow-hidden group">
                    <div class="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div class="flex justify-between items-center mb-2">
                        <h5 class="text-xs uppercase tracking-wider text-purple-400 font-cinzel font-semibold"><i class="fa-solid fa-font mr-1.5"></i> 2. Romaji (คำอ่านโรมะจิ)</h5>
                        <button id="modal-copy-romaji-btn" class="text-xs text-purple-400 hover:text-purple-300 font-cinzel"><i class="fa-regular fa-copy"></i> Copy</button>
                    </div>
                    <p id="modal-romaji-chant" class="text-sm sm:text-base text-magic-gold-light leading-relaxed italic">...</p>
                </div>

                <!-- 3. Thai Chant -->
                <div class="bg-black/40 rounded-xl p-5 border-l-4 border-magic-gold relative overflow-hidden group">
                    <div class="absolute inset-0 bg-gradient-to-r from-magic-gold/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div class="flex justify-between items-center mb-2">
                        <h5 class="text-xs uppercase tracking-wider text-magic-gold font-cinzel font-semibold"><i class="fa-solid fa-book mr-1.5"></i> 3. Thai (คำแปลภาษาไทย)</h5>
                        <button id="modal-copy-th-btn" class="text-xs text-magic-gold hover:text-yellow-300 font-cinzel"><i class="fa-regular fa-copy"></i> Copy</button>
                    </div>
                    <p id="modal-thai-chant" class="text-base sm:text-lg text-gray-200 leading-relaxed font-light italic">"..."</p>
                </div>

                <!-- Spell Effect & Mechanics -->
                <div class="bg-black/30 rounded-xl p-4 border border-white/5 flex flex-col sm:flex-row justify-between gap-3 text-xs text-gray-400">
                    <div><strong>MP Cost:</strong> <span id="modal-mp-cost" class="text-cyan-400"></span></div>
                    <div><strong>Rank:</strong> <span id="modal-rank-text" class="text-yellow-400"></span></div>
                    <div><strong>Casters:</strong> <span id="modal-casters-text" class="text-white"></span></div>
                </div>

                <div class="text-center pt-2">
                    <button id="modal-practice-btn" class="w-full py-3 rounded-xl bg-gradient-to-r from-magic-gold to-yellow-500 text-magic-dark font-cinzel font-bold text-sm uppercase tracking-wider hover:scale-[1.02] transition-transform">
                        <i class="fa-solid fa-dumbbell mr-2"></i> Practice This Spell In Training Mode
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Battle Chanting Modal -->
    <div id="battle-chant-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-md" onclick="closeBattleChantModal()"></div>
        <div class="modal-content relative w-full max-w-lg rounded-2xl p-6 text-center z-10">
            <h4 class="text-xs uppercase tracking-widest text-magic-gold font-cinzel mb-1">Chanting Phase</h4>
            <h3 id="battle-chant-spell-name" class="font-cinzel text-2xl font-bold text-white mb-4">Spell Name</h3>

            <div class="bg-black/60 border border-magic-gold/30 rounded-xl p-4 text-left mb-4">
                <div id="battle-chant-jp" class="font-jp text-lg text-white font-bold leading-relaxed mb-2"></div>
                <div id="battle-chant-romaji" class="text-sm text-magic-gold-light italic"></div>
            </div>

            <div class="flex justify-center mb-4">
                <button id="battle-mic-btn" onclick="toggleBattleSpeech()" class="w-16 h-16 rounded-full bg-white/5 border-2 border-magic-gold text-magic-gold text-2xl flex items-center justify-center hover:bg-magic-gold/20">
                    <i class="fa-solid fa-microphone"></i>
                </button>
            </div>
            <div id="battle-transcript-text" class="text-xs text-gray-400 mb-4 min-h-[30px]">Press mic and chant to cast!</div>

            <button onclick="instantCastBattleSpell()" class="w-full py-2 bg-white/10 hover:bg-white/20 text-xs text-gray-300 font-cinzel uppercase tracking-wider rounded-lg border border-white/10">
                Fast Cast (Skip Mic)
            </button>
        </div>
    </div>

    <!-- ======================================================== -->
    <!-- JAVASCRIPT LOGIC -->
    <!-- ======================================================== -->
    <script>
        const spellsData = ''' + json.dumps(spells, ensure_ascii=False) + ''';

        // TAB SWITCHER
        function switchTab(tab) {
            document.getElementById('view-grimoire').classList.add('hidden');
            document.getElementById('view-training').classList.add('hidden');
            document.getElementById('view-battle').classList.add('hidden');

            document.getElementById('tab-btn-grimoire').className = "px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold";
            document.getElementById('tab-btn-training').className = "px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold";
            document.getElementById('tab-btn-battle').className = "px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold/30 bg-magic-blue/60 text-gray-300 hover:text-white hover:border-magic-gold";

            if (tab === 'grimoire') {
                document.getElementById('view-grimoire').classList.remove('hidden');
                document.getElementById('tab-btn-grimoire').className = "px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]";
            } else if (tab === 'training') {
                document.getElementById('view-training').classList.remove('hidden');
                document.getElementById('tab-btn-training').className = "px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]";
            } else if (tab === 'battle') {
                document.getElementById('view-battle').classList.remove('hidden');
                document.getElementById('tab-btn-battle').className = "px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]";
            }
        }

        // =========================================================
        // 1. GRIMOIRE CARD RENDER (Exact firstOne.html design)
        // =========================================================
        function renderSpells(dataToRender = spellsData) {
            const grid = document.getElementById('spell-grid');
            grid.classList.add('grid-fade-out');
            grid.classList.remove('grid-fade-in');

            setTimeout(() => {
                grid.innerHTML = '';
                if (dataToRender.length === 0) {
                    grid.innerHTML = '<div class="col-span-full text-center text-gray-500 py-12 font-cinzel text-xl">No spells found matching the criteria.</div>';
                }

                dataToRender.forEach((spell) => {
                    let accentColor = 'bg-gray-500';
                    if (spell.element === 'Water') accentColor = 'bg-blue-500';
                    else if (spell.element === 'Fire') accentColor = 'bg-red-500';
                    else if (spell.element === 'Earth') accentColor = 'bg-amber-700';
                    else if (spell.element === 'Healing') accentColor = 'bg-yellow-400';
                    else if (spell.element === 'Dragon') accentColor = 'bg-rose-500';

                    const cardHTML = `
                        <div class="spell-card rounded-xl p-6 relative overflow-hidden flex flex-col h-full group" onclick="openModal(${spell.id})">
                            <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-white/5 to-transparent rounded-bl-full pointer-events-none"></div>
                            
                            <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center">
                                    <div class="w-2 h-2 rounded-full ${accentColor} mr-2.5 shadow-[0_0_8px_currentColor]"></div>
                                    <span class="text-xs text-gray-400 uppercase tracking-wider font-semibold">${spell.rank}</span>
                                </div>
                                <span class="text-[10px] text-magic-gold/80 font-cinzel px-2 py-0.5 rounded bg-magic-gold/10 border border-magic-gold/20">${spell.element}</span>
                            </div>
                            
                            <h3 class="font-cinzel text-2xl font-bold text-magic-gold-light mb-0.5 group-hover:text-magic-gold transition-colors">${spell.en}</h3>
                            <h4 class="text-magic-gold-light/90 text-sm mb-4 font-medium tracking-wide">${spell.romaji_name} <span class="text-gray-500 text-xs font-jp">(${spell.jp_name})</span></h4>
                            
                            <div class="mt-auto">
                                <p class="text-gray-300 text-xs sm:text-sm line-clamp-3 italic opacity-85 border-l-2 border-magic-gold/30 pl-3">
                                    "${spell.romaji}"
                                </p>
                            </div>
                            
                            <div class="absolute bottom-4 right-4 w-1 h-1 bg-magic-gold rounded-full opacity-0 group-hover:opacity-100 animate-ping"></div>
                        </div>
                    `;
                    grid.insertAdjacentHTML('beforeend', cardHTML);
                });

                requestAnimationFrame(() => {
                    grid.classList.remove('grid-fade-out');
                    grid.classList.add('grid-fade-in');
                });
            }, 250);
        }

        const elementOrder = {
            'Water': 1,
            'Fire': 2,
            'Earth': 3,
            'Healing': 4,
            'Dragon': 5
        };

        function getSpellRankWeight(rankStr) {
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

        function applyFiltersAndSort() {
            const sortVal = document.getElementById('sort-select').value;
            const filterVal = document.getElementById('filter-select').value;
            const searchVal = document.getElementById('search-input').value.toLowerCase().trim();

            let processed = spellsData.filter(spell => {
                const matchFilter = (filterVal === 'all') || (spell.element.toLowerCase() === filterVal.toLowerCase());
                const matchSearch = !searchVal || 
                    spell.en.toLowerCase().includes(searchVal) ||
                    (spell.romaji_name && spell.romaji_name.toLowerCase().includes(searchVal)) ||
                    (spell.jp_name && spell.jp_name.includes(searchVal)) ||
                    spell.name.toLowerCase().includes(searchVal) ||
                    spell.jp.includes(searchVal) ||
                    spell.romaji.toLowerCase().includes(searchVal) ||
                    spell.th.includes(searchVal);
                return matchFilter && matchSearch;
            });

            processed.sort((a, b) => {
                if (sortVal === 'element') {
                    const elemDiff = (elementOrder[a.element] || 99) - (elementOrder[b.element] || 99);
                    if (elemDiff !== 0) return elemDiff;
                    const rankDiff = getSpellRankWeight(a.rank) - getSpellRankWeight(b.rank);
                    if (rankDiff !== 0) return rankDiff;
                    return a.mp_cost - b.mp_cost;
                }
                if (sortVal === 'level') {
                    const rankDiff = getSpellRankWeight(a.rank) - getSpellRankWeight(b.rank);
                    if (rankDiff !== 0) return rankDiff;
                    return a.mp_cost - b.mp_cost;
                }
                if (sortVal === 'id') {
                    return a.id - b.id;
                }
                // Default: Element & Tier
                const elemDiff = (elementOrder[a.element] || 99) - (elementOrder[b.element] || 99);
                if (elemDiff !== 0) return elemDiff;
                const rankDiff = getSpellRankWeight(a.rank) - getSpellRankWeight(b.rank);
                if (rankDiff !== 0) return rankDiff;
                return a.mp_cost - b.mp_cost;
            });

            renderSpells(processed);
        }

        // MODAL FUNCTIONS
        const modal = document.getElementById('spell-modal');
        const mTitle = document.getElementById('modal-title');
        const mRomajiTitle = document.getElementById('modal-romaji-title');
        const mThaiTitle = document.getElementById('modal-thai-title');
        const mType = document.getElementById('modal-type');
        const mJpChant = document.getElementById('modal-jp-chant');
        const mRomajiChant = document.getElementById('modal-romaji-chant');
        const mThaiChant = document.getElementById('modal-thai-chant');
        const mMpCost = document.getElementById('modal-mp-cost');
        const mRankText = document.getElementById('modal-rank-text');
        const mCastersText = document.getElementById('modal-casters-text');
        const mPracticeBtn = document.getElementById('modal-practice-btn');

        function openModal(id) {
            const spell = spellsData.find(s => s.id === id);
            if (!spell) return;

            mTitle.textContent = spell.en;
            mRomajiTitle.textContent = `${spell.romaji_name} (${spell.jp_name})`;
            mThaiTitle.textContent = spell.name.split('(')[0].trim();
            mType.textContent = `${spell.rank} • ${spell.element_th || spell.element}`;
            mJpChant.textContent = spell.jp;
            mRomajiChant.textContent = spell.romaji;
            mThaiChant.textContent = `"${spell.th}"`;
            mMpCost.textContent = `${spell.mp_cost} MP`;
            mRankText.textContent = spell.rank;
            mCastersText.textContent = spell.casters.join(', ');

            document.getElementById('modal-copy-jp-btn').onclick = () => copyText(spell.jp, 'Japanese Chant');
            document.getElementById('modal-copy-romaji-btn').onclick = () => copyText(spell.romaji, 'Romaji Chant');
            document.getElementById('modal-copy-th-btn').onclick = () => copyText(spell.th, 'Thai Chant');
            document.getElementById('modal-play-voice-btn').onclick = () => playVoice(spell.jp);

            mPracticeBtn.onclick = () => {
                closeModal();
                startSingleTraining(spell.id);
            };

            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !modal.classList.contains('hidden')) closeModal();
        });

        // =========================================================
        // 2. TRAINING MODE (JP + ROMAJI ONLY)
        // =========================================================
        let trainingQueue = [];
        let trainCurrentIndex = 0;
        let isTrainingRecording = false;

        function generateTrainingQueue() {
            const elem = document.getElementById('train-element-select').value;
            const t1Count = parseInt(document.getElementById('train-tier1-count').value) || 0;
            const t2Count = parseInt(document.getElementById('train-tier2-count').value) || 0;

            let pool = spellsData;
            if (elem !== 'All') {
                pool = pool.filter(s => s.element.toLowerCase() === elem.toLowerCase());
            }

            const t1 = [...pool.filter(s => s.tier === 'tier1')].sort(() => Math.random() - 0.5).slice(0, t1Count);
            const t2 = [...pool.filter(s => s.tier === 'tier2')].sort(() => Math.random() - 0.5).slice(0, t2Count);

            trainingQueue = [...t1, ...t2];
            if (trainingQueue.length === 0) {
                alert('No spells match this element and tier count combination.');
                return;
            }

            trainCurrentIndex = 0;
            displayTrainingCard();
            document.getElementById('training-stage-box').classList.remove('hidden');
            document.getElementById('training-stage-box').scrollIntoView({ behavior: 'smooth' });
        }

        function startSingleTraining(id) {
            const spell = spellsData.find(s => s.id === id);
            if (!spell) return;
            trainingQueue = [spell];
            trainCurrentIndex = 0;
            switchTab('training');
            displayTrainingCard();
            document.getElementById('training-stage-box').classList.remove('hidden');
            document.getElementById('training-stage-box').scrollIntoView({ behavior: 'smooth' });
        }

        function displayTrainingCard() {
            if (trainCurrentIndex < 0 || trainCurrentIndex >= trainingQueue.length) return;
            const s = trainingQueue[trainCurrentIndex];

            document.getElementById('train-counter').textContent = `STAGE ${trainCurrentIndex + 1} / ${trainingQueue.length} (${s.rank})`;
            document.getElementById('train-spell-name').textContent = s.en;
            document.getElementById('train-jp-text').textContent = `「${s.jp}」`;
            document.getElementById('train-romaji-text').textContent = s.romaji;
            document.getElementById('train-transcript-box').innerHTML = `<span>Press microphone button and chant in Japanese or Romaji...</span>`;
            document.getElementById('train-result-badge').innerHTML = '';
            document.getElementById('train-mic-btn').classList.remove('recording-pulse');

            document.getElementById('train-prev-btn').disabled = (trainCurrentIndex === 0);
            document.getElementById('train-next-btn').disabled = (trainCurrentIndex === trainingQueue.length - 1);
        }

        function navigateTraining(delta) {
            trainCurrentIndex += delta;
            if (trainCurrentIndex < 0) trainCurrentIndex = 0;
            if (trainCurrentIndex >= trainingQueue.length) trainCurrentIndex = trainingQueue.length - 1;
            displayTrainingCard();
        }

        function playCurrentTrainingAudio() {
            const s = trainingQueue[trainCurrentIndex];
            if (s) playVoice(s.jp);
        }

        // SPEECH RECOGNITION (Accent Tolerant)
        let recognition = null;
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRec();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'ja-JP';
        }

        function toggleTrainingSpeech() {
            if (!recognition) {
                const manual = prompt('Speech Recognition not supported in this browser. Enter chant transcript:');
                if (manual) evaluateTrainingChant(manual);
                return;
            }

            const micBtn = document.getElementById('train-mic-btn');
            const box = document.getElementById('train-transcript-box');

            if (isTrainingRecording) {
                recognition.stop();
                isTrainingRecording = false;
                micBtn.classList.remove('recording-pulse');
            } else {
                recognition.start();
                isTrainingRecording = true;
                micBtn.classList.add('recording-pulse');
                box.innerHTML = `<span class="text-magic-gold animate-pulse"><i class="fa-solid fa-ear-listen mr-2"></i>Listening to mana resonance...</span>`;

                recognition.onresult = (e) => {
                    let transcript = '';
                    for (let i = e.resultIndex; i < e.results.length; ++i) {
                        transcript += e.results[i][0].transcript;
                    }
                    box.innerHTML = `<span class="text-white">Heard: "${transcript}"</span>`;
                    if (e.results[0].isFinal) {
                        evaluateTrainingChant(transcript);
                    }
                };

                recognition.onerror = () => {
                    isTrainingRecording = false;
                    micBtn.classList.remove('recording-pulse');
                    box.innerHTML = `<span class="text-red-400">Microphone detection error.</span>`;
                };

                recognition.onend = () => {
                    isTrainingRecording = false;
                    micBtn.classList.remove('recording-pulse');
                };
            }
        }

        function evaluateTrainingChant(spoken) {
            const spell = trainingQueue[trainCurrentIndex];
            const cleanSpoken = spoken.replace(/[「」『』、。・\\s!?]/g, '').toLowerCase();
            const cleanTarget = spell.jp.replace(/[「」『』、。・\\s!?]/g, '').toLowerCase();

            // Extract magic anchor keywords
            const anchors = [];
            if (spell.jp.includes('水の精霊')) anchors.push('水の精霊', '水');
            if (spell.jp.includes('雷帝')) anchors.push('雷帝');
            if (spell.jp.includes('神なる力')) anchors.push('神なる力', '神');
            if (spell.jp.includes('キュムロニンバス')) anchors.push('キュムロニンバス', 'cumulonimbus');
            if (spell.jp.includes('ウォーター')) anchors.push('ウォーター', 'water');
            if (spell.jp.includes('ライトニング')) anchors.push('ライトニング', 'lightning');
            if (spell.jp.includes('ヒーリング')) anchors.push('ヒーリング', 'healing');

            let matchCount = 0;
            anchors.forEach(a => { if (cleanSpoken.includes(a.toLowerCase())) matchCount++; });

            let charMatches = 0;
            for (const ch of cleanSpoken) {
                if (cleanTarget.includes(ch)) charMatches++;
            }
            const ratio = cleanTarget.length > 0 ? (charMatches / cleanTarget.length) : 0;
            const badge = document.getElementById('train-result-badge');

            if (ratio >= 0.75 || (anchors.length > 0 && matchCount >= anchors.length * 0.5 && ratio >= 0.45)) {
                badge.innerHTML = `
                    <div class="inline-block px-4 py-2 rounded-full bg-green-500/20 border border-green-500 text-green-300 font-cinzel text-sm">
                        <i class="fa-solid fa-circle-check mr-2"></i> S-RANK: PERFECT SPELL CHANT!
                    </div>
                `;
            } else if (matchCount > 0 || ratio >= 0.3 || cleanSpoken.includes(spell.en.toLowerCase())) {
                badge.innerHTML = `
                    <div class="inline-block px-4 py-2 rounded-full bg-yellow-500/20 border border-yellow-500 text-yellow-300 font-cinzel text-sm">
                        <i class="fa-solid fa-triangle-exclamation mr-2"></i> A-RANK / PASS: ACCENT TOLERATED (Spell Success)
                    </div>
                `;
            } else {
                badge.innerHTML = `
                    <div class="inline-block px-4 py-2 rounded-full bg-red-500/20 border border-red-500 text-red-300 font-cinzel text-sm">
                        <i class="fa-solid fa-xmark mr-2"></i> FIZZLE / TRY AGAIN (Mana Disrupted)
                    </div>
                `;
            }
        }

        // =========================================================
        // 3. BALANCED BATTLE RPG ENGINE
        // =========================================================
        const enemies = {
            crawler: { name: "Iron Crawler", maxHp: 750, atk: 45, weak: ["Water", "Ice", "Lightning"], resist: ["Earth"], desc: "Labyrinth creature with heavy shell. Weak to Water Splash + Freeze combos!", type: "Heavy Armor", icon: "fa-bug" },
            treant: { name: "Forest Treant", maxHp: 900, atk: 50, weak: ["Fire"], resist: ["Water", "Earth"], desc: "Towering ancient wood beast. Extreme vulnerability to Fire magic!", type: "Plant Spirit", icon: "fa-tree" },
            salamander: { name: "Magma Salamander", maxHp: 800, atk: 60, weak: ["Water", "Ice"], resist: ["Fire"], desc: "Blazing reptile. Water and Ice spells inflict critical damage!", type: "Flame Beast", icon: "fa-fire" },
            wyvern: { name: "Red Wyvern", maxHp: 1300, atk: 80, weak: ["Lightning", "Dragon"], resist: ["Fire"], desc: "Apex aerial beast. Requires Cumulonimbus, Lightning, or Dragon Gates!", type: "Dragon Race", icon: "fa-dragon" }
        };

        let battleState = {
            playerHp: 500, playerMaxHp: 500,
            playerMp: 350, playerMaxMp: 350,
            enemyKey: 'crawler', enemyHp: 750, enemyMaxHp: 750,
            turn: 1, soaked: false, isOver: false,
            deck: [2, 8, 6, 16],
            selectedSpell: null
        };

        function initBattle() {
            const key = document.getElementById('battle-enemy-select').value;
            const e = enemies[key];
            battleState.enemyKey = key;
            battleState.playerHp = battleState.playerMaxHp;
            battleState.playerMp = battleState.playerMaxMp;
            battleState.enemyHp = e.maxHp;
            battleState.enemyMaxHp = e.maxHp;
            battleState.turn = 1;
            battleState.soaked = false;
            battleState.isOver = false;

            if (key === 'treant') battleState.deck = [18, 11, 13, 5];
            else if (key === 'crawler') battleState.deck = [8, 9, 6, 16];
            else if (key === 'salamander') battleState.deck = [2, 12, 10, 3];
            else battleState.deck = [3, 16, 14, 19];

            document.getElementById('enemy-name-text').innerHTML = `<i class="fa-solid ${e.icon} text-red-400 mr-2"></i>${e.name}`;
            document.getElementById('enemy-type-badge').textContent = e.type;
            document.getElementById('enemy-weakness-text').textContent = `Weak: ${e.weak.join(' / ')}`;
            document.getElementById('enemy-desc-text').textContent = e.desc;

            updateBattleUI();
            renderBattleSlots();
            document.getElementById('battle-log-box').innerHTML = `<div>[ENCOUNTER] A ferocious <strong>${e.name}</strong> emerged from the darkness!</div>`;
        }

        function updateBattleUI() {
            document.getElementById('player-hp-text').textContent = `${Math.max(0, battleState.playerHp)} / ${battleState.playerMaxHp}`;
            document.getElementById('player-hp-bar').style.width = `${Math.max(0, (battleState.playerHp / battleState.playerMaxHp) * 100)}%`;

            document.getElementById('player-mp-text').textContent = `${Math.max(0, battleState.playerMp)} / ${battleState.playerMaxMp}`;
            document.getElementById('player-mp-bar').style.width = `${Math.max(0, (battleState.playerMp / battleState.playerMaxMp) * 100)}%`;

            document.getElementById('enemy-hp-text').textContent = `${Math.max(0, battleState.enemyHp)} / ${battleState.enemyMaxHp}`;
            document.getElementById('enemy-hp-bar').style.width = `${Math.max(0, (battleState.enemyHp / battleState.enemyMaxHp) * 100)}%`;

            document.getElementById('battle-turn-count').textContent = battleState.turn;
        }

        function renderBattleSlots() {
            const container = document.getElementById('battle-slots-container');
            container.innerHTML = '';
            battleState.deck.forEach(id => {
                const s = spellsData.find(sp => sp.id === id);
                if (!s) return;

                const btn = document.createElement('button');
                btn.className = "bg-magic-dark/80 hover:bg-magic-dark border border-magic-gold/30 hover:border-magic-gold p-3 rounded-xl text-left transition-all flex flex-col justify-between";
                btn.innerHTML = `
                    <div class="flex justify-between items-center w-full mb-1">
                        <span class="font-cinzel text-sm font-bold text-white">${s.en}</span>
                        <span class="text-xs text-cyan-400 font-bold">${s.mp_cost} MP</span>
                    </div>
                    <div class="text-[11px] text-gray-400">${s.rank} • ${s.element} (Pwr: ${s.power})</div>
                `;
                btn.onclick = () => openBattleChantModal(s);
                container.appendChild(btn);
            });
        }

        function openBattleChantModal(spell) {
            if (battleState.isOver) return;
            if (battleState.playerMp < spell.mp_cost) {
                logBattle(`<span class="text-red-400">[LOW MP] Need ${spell.mp_cost} MP to cast ${spell.en}!</span>`);
                return;
            }

            battleState.selectedSpell = spell;
            document.getElementById('battle-chant-spell-name').textContent = spell.en;
            document.getElementById('battle-chant-jp').textContent = `「${spell.jp}」`;
            document.getElementById('battle-chant-romaji').textContent = spell.romaji;
            document.getElementById('battle-transcript-text').textContent = "Press mic and chant to cast!";
            document.getElementById('battle-mic-btn').classList.remove('recording-pulse');

            document.getElementById('battle-chant-modal').classList.remove('hidden');
        }

        function closeBattleChantModal() {
            document.getElementById('battle-chant-modal').classList.add('hidden');
        }

        function toggleBattleSpeech() {
            if (!recognition) {
                instantCastBattleSpell();
                return;
            }

            const micBtn = document.getElementById('battle-mic-btn');
            const txt = document.getElementById('battle-transcript-text');

            recognition.start();
            micBtn.classList.add('recording-pulse');
            txt.textContent = "Chanting... Speak now!";

            recognition.onresult = (e) => {
                const transcript = e.results[0][0].transcript;
                txt.textContent = `Heard: "${transcript}"`;
                setTimeout(() => {
                    closeBattleChantModal();
                    castSpellInBattle(battleState.selectedSpell);
                }, 500);
            };
        }

        function instantCastBattleSpell() {
            closeBattleChantModal();
            castSpellInBattle(battleState.selectedSpell);
        }

        function castSpellInBattle(spell) {
            if (!spell || battleState.isOver) return;
            battleState.playerMp -= spell.mp_cost;

            const e = enemies[battleState.enemyKey];
            let multiplier = 1.0;
            if (e.weak.some(w => spell.element.toLowerCase().includes(w.toLowerCase()))) multiplier *= 2.0;
            if (e.resist.some(r => spell.element.toLowerCase().includes(r.toLowerCase()))) multiplier *= 0.5;

            // Synergy combo: Water Splash soaked + Ice/Thunder
            let isCombo = false;
            if (battleState.soaked && (spell.en.includes('Ice') || spell.en.includes('Icicle') || spell.en.includes('Lightning') || spell.en.includes('Blizzard'))) {
                isCombo = true;
                multiplier *= 1.8;
                battleState.soaked = false;
            }

            if (spell.type === 'setup') battleState.soaked = true;

            const dmg = Math.round(spell.power * multiplier * (0.9 + Math.random() * 0.25));

            if (spell.type === 'heal') {
                battleState.playerHp = Math.min(battleState.playerMaxHp, battleState.playerHp + spell.power * 2);
                logBattle(`[RESTORE] Chanted <strong>${spell.en}</strong>! Restored <span class="text-green-400">+${spell.power * 2} HP</span>!`);
            } else {
                battleState.enemyHp -= dmg;
                if (isCombo) logBattle(`<span class="text-purple-400 font-bold">[FROST NOVA COMBO!]</span> Soaked target shattered! Dealt <strong class="text-yellow-300">${dmg} DMG</strong>!`);
                else if (multiplier >= 2.0) logBattle(`<span class="text-yellow-400 font-bold">[SUPER EFFECTIVE!]</span> ${spell.en} struck weakness! Dealt <strong class="text-yellow-300">${dmg} DMG</strong>!`);
                else logBattle(`[SPELL CAST] Chanted <strong>${spell.en}</strong>! Dealt ${dmg} damage to ${e.name}.`);
            }

            updateBattleUI();

            if (battleState.enemyHp <= 0) {
                battleState.isOver = true;
                evaluateBattleRank();
                return;
            }

            // Enemy Turn
            setTimeout(() => {
                if (battleState.isOver) return;
                const eDmg = Math.round(e.atk * (0.8 + Math.random() * 0.4));
                battleState.playerHp -= eDmg;
                logBattle(`<span class="text-red-400">[ENEMY ATTACK]</span> ${e.name} struck you for ${eDmg} damage!`);
                battleState.turn++;
                updateBattleUI();

                if (battleState.playerHp <= 0) {
                    battleState.isOver = true;
                    logBattle(`<span class="text-red-500 font-bold">[DEFEAT] You collapsed! Rank: F</span>`);
                }
            }, 600);
        }

        function triggerQuickVoiceBattle() {
            const spellName = prompt("QUICK CAST: Enter spell name or part of chant (e.g. Cumulonimbus, Water Ball, Lightning):");
            if (!spellName) return;
            const found = spellsData.find(s => s.en.toLowerCase().includes(spellName.toLowerCase()) || s.jp.includes(spellName) || s.romaji.toLowerCase().includes(spellName.toLowerCase()));
            if (found) {
                logBattle(`<span class="text-cyan-400 font-bold">[QUICK VOICE CAST]</span> Instantaneous mana release for <strong>${found.en}</strong>!`);
                castSpellInBattle(found);
            } else {
                logBattle(`<span class="text-red-400">[UNKNOWN INCANTATION]</span> No matching spell found for "${spellName}".`);
            }
        }

        function logBattle(msg) {
            const b = document.getElementById('battle-log-box');
            b.innerHTML += `<div>${msg}</div>`;
            b.scrollTop = b.scrollHeight;
        }

        function evaluateBattleRank() {
            let rank = 'B';
            if (battleState.turn <= 3 && battleState.playerHp >= 350) rank = 'S (Divine Archmage)';
            else if (battleState.turn <= 5) rank = 'A (Saint Class)';
            else if (battleState.turn <= 8) rank = 'B (Advanced Class)';
            else rank = 'C (Apprentice)';

            logBattle(`
                <div class="bg-yellow-500/20 border border-magic-gold p-3 rounded-lg my-2 text-center text-magic-gold">
                    <div class="text-base font-bold"><i class="fa-solid fa-trophy mr-1"></i> VICTORY! Evaluation Rank: ${rank}</div>
                    <div class="text-xs text-gray-300">Turns: ${battleState.turn} • HP Left: ${battleState.playerHp}</div>
                </div>
            `);
        }

        // UTILITIES
        function playVoice(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const u = new SpeechSynthesisUtterance(text);
                u.lang = 'ja-JP';
                u.rate = 0.9;
                window.speechSynthesis.speak(u);
            }
        }

        function copyText(txt, label) {
            navigator.clipboard.writeText(txt).then(() => alert(`Copied ${label} to clipboard!`));
        }

        // Particle Canvas
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() { this.reset(); }
            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedY = -(Math.random() * 0.3 + 0.1);
                this.color = Math.random() > 0.5 ? '197, 160, 89' : '56, 189, 248';
                this.alpha = Math.random() * 0.5 + 0.1;
            }
            update() {
                this.y += this.speedY;
                if (this.y < 0) this.y = canvas.height;
            }
            draw() {
                ctx.fillStyle = `rgba(${this.color}, ${this.alpha})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        for (let i = 0; i < 45; i++) particles.push(new Particle());
        function anim() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(anim);
        }
        anim();

        // INIT
        window.addEventListener('DOMContentLoaded', () => {
            applyFiltersAndSort();
            initBattle();
        });
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Generated unified index.html successfully with firstOne.html card design!')
