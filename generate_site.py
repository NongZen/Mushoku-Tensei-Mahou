import json

with open('data.json', 'r', encoding='utf-8') as f:
    spells = json.load(f)

# Build HTML template with transparent circular favicon + full chant voice detection (no syllable dividing)
html = '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mushoku Tensei: Magic Chants & Combat Grimoire</title>
    
    <!-- Circular transparent favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon.png">
    <link rel="apple-touch-icon" href="icon.png">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Noto+Serif+JP:wght@400;600;700;900&family=Prompt:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Transformers.js for In-Browser Web AI Whisper -->
    <script type="module">
        import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2';
        env.allowLocalModels = false;
        window.transformersPipeline = pipeline;
    </script>

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
        #spell-modal, #training-modal, #battle-chant-modal, #engine-settings-modal {
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }
        #spell-modal.hidden, #training-modal.hidden, #battle-chant-modal.hidden, #engine-settings-modal.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        #spell-modal:not(.hidden), #training-modal:not(.hidden), #battle-chant-modal:not(.hidden), #engine-settings-modal:not(.hidden) {
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
        
        #spell-modal:not(.hidden) .modal-content, #training-modal:not(.hidden) .modal-content, #battle-chant-modal:not(.hidden) .modal-content, #engine-settings-modal:not(.hidden) .modal-content {
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
        }
    </style>
</head>
<body class="font-prompt min-h-screen relative overflow-x-hidden antialiased">

    <!-- Ambient Particles Canvas -->
    <canvas id="particle-canvas" class="fixed inset-0 pointer-events-none z-0 opacity-40"></canvas>

    <div class="container mx-auto px-4 py-8 relative z-10 max-w-7xl">
        
        <!-- Header -->
        <header class="text-center mb-10">
            <div class="inline-block relative mb-4 group">
                <div class="absolute -inset-1.5 bg-gradient-to-r from-magic-gold via-yellow-300 to-magic-gold rounded-full blur-md opacity-40 group-hover:opacity-75 transition duration-500"></div>
                <img src="icon.png" alt="Mushoku Tensei Emblem" class="relative w-28 h-28 md:w-32 md:h-32 mx-auto rounded-full border-2 border-magic-gold shadow-[0_0_20px_rgba(197,160,89,0.4)] object-cover transform group-hover:scale-105 transition-all duration-300 cursor-pointer">
            </div>
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
        <!-- VIEW 1: GRIMOIRE CARDS (firstOne.html design) -->
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

            <!-- Grimoire Cards Grid -->
            <div id="spell-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 transition-all duration-300">
                <!-- Cards injected dynamically via JS -->
            </div>
        </section>

        <!-- ======================================================== -->
        <!-- VIEW 2: CHANTING TRAINING (FULL CHANT RECITATION) -->
        <!-- ======================================================== -->
        <section id="view-training" class="hidden">
            <!-- Training Queue Generator Configuration -->
            <div class="bg-gradient-to-b from-[#111a24] to-[#0d121c] border-2 border-magic-gold/40 rounded-3xl p-6 md:p-8 backdrop-blur-md max-w-4xl mx-auto mb-10 shadow-2xl">
                <div class="text-center mb-6">
                    <h3 class="font-cinzel text-2xl font-bold text-white mb-2 text-glow"><i class="fa-solid fa-graduation-cap text-magic-gold mr-2"></i>Chanting Academy (JP & Romaji)</h3>
                    <p class="text-gray-400 text-sm">สร้างคิวฝึกซ้อมร่ายเวทมนตร์ ร่ายทั้งบทสวดเต็มบทเพื่อความสมจริง</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div class="bg-magic-dark/60 border border-magic-gold/20 p-4 rounded-xl">
                        <label class="block text-xs uppercase text-gray-400 font-cinzel mb-2">Target Element (ธาตุเป้าหมาย):</label>
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
                
                <!-- Voice Engine Selector Pill -->
                <div class="flex flex-wrap items-center justify-center gap-2 mb-6 bg-black/50 p-2 rounded-2xl border border-magic-gold/20 max-w-xl mx-auto">
                    <span class="text-[11px] uppercase font-cinzel text-gray-400 mr-1"><i class="fa-solid fa-microchip text-magic-gold mr-1"></i> ASR Engine:</span>
                    <button onclick="setVoiceEngine('stream')" id="engine-btn-stream" class="px-3 py-1.5 rounded-xl text-xs font-cinzel border border-magic-gold bg-magic-gold text-magic-dark font-bold transition-all shadow-[0_0_10px_rgba(197,160,89,0.3)]">
                        <i class="fa-solid fa-bolt mr-1"></i> 1. Live Web Speech
                    </button>
                    <button onclick="setVoiceEngine('cloud')" id="engine-btn-cloud" class="px-3 py-1.5 rounded-xl text-xs font-cinzel border border-white/10 bg-white/5 text-gray-300 hover:text-white transition-all">
                        <i class="fa-solid fa-cloud mr-1"></i> 2. Serverless Whisper
                    </button>
                    <button onclick="setVoiceEngine('browser_ai')" id="engine-btn-browser_ai" class="px-3 py-1.5 rounded-xl text-xs font-cinzel border border-white/10 bg-white/5 text-gray-300 hover:text-white transition-all">
                        <i class="fa-solid fa-robot mr-1"></i> 3. Web AI (Offline)
                    </button>
                    <button onclick="openEngineSettings()" class="text-xs text-magic-gold hover:text-yellow-300 p-1.5 rounded-lg bg-white/5 border border-white/10 ml-1" title="API Settings">
                        <i class="fa-solid fa-gear"></i>
                    </button>
                </div>

                <!-- Web AI Model Download Progress Indicator -->
                <div id="model-loading-box" class="hidden mb-6 bg-blue-950/60 border border-blue-400/40 rounded-2xl p-4 max-w-xl mx-auto text-xs text-blue-200">
                    <div class="flex justify-between items-center mb-1.5">
                        <span id="model-loading-status"><i class="fa-solid fa-spinner fa-spin mr-2"></i> Loading Web AI Model (Xenova/whisper-tiny)...</span>
                        <span id="model-loading-percent" class="font-bold text-white">0%</span>
                    </div>
                    <div class="w-full bg-black/60 rounded-full h-2 overflow-hidden border border-blue-500/30">
                        <div id="model-loading-bar" class="bg-gradient-to-r from-blue-400 to-cyan-300 h-full rounded-full transition-all duration-200" style="width: 0%;"></div>
                    </div>
                </div>

                <div id="train-counter" class="font-cinzel text-magic-gold text-xs tracking-widest uppercase mb-1">STAGE 1 / 2</div>
                <h3 id="train-spell-name" class="font-cinzel text-2xl md:text-3xl font-bold text-white mb-4 text-glow">Water Ball</h3>

                <!-- Active Chant Box (Full Chant) -->
                <div class="bg-black/60 border border-magic-gold/30 rounded-2xl p-5 md:p-7 mb-6 text-left">
                    <div class="text-xs uppercase text-gray-400 font-cinzel mb-2">Full Japanese Incantation:</div>
                    <div id="train-jp-text" class="font-jp text-lg md:text-xl text-white font-bold leading-relaxed mb-3">
                        「汝の求める所に大いなる水の加護あらん、清涼なるせせらぎの流れを今ここに、ウォーターボール」
                    </div>
                    <div class="text-xs uppercase text-magic-gold font-cinzel mb-1">Romaji:</div>
                    <div id="train-romaji-text" class="text-sm md:text-base text-magic-gold-light italic leading-relaxed">
                        Nanji no motomeru tokoro ni oinaru mizu no kago aran, seiryo naru seseragi no nagare o ima koko ni, Wota Boru
                    </div>
                </div>

                <!-- Mic and Audio Controls -->
                <div class="flex justify-center items-center gap-4 mb-5">
                    <button id="train-mic-btn" onclick="toggleTrainingSpeech()" class="w-16 h-16 rounded-full bg-white/5 border-2 border-magic-gold text-magic-gold text-2xl flex items-center justify-center hover:bg-magic-gold/20 hover:scale-105 transition-all shadow-[0_0_15px_rgba(197,160,89,0.2)]">
                        <i class="fa-solid fa-microphone"></i>
                    </button>
                    <button onclick="playCurrentTrainingAudio()" class="px-5 py-3 rounded-xl bg-magic-blue/80 border border-magic-gold/40 text-gray-200 hover:text-white hover:border-magic-gold text-xs font-cinzel uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-volume-high text-magic-gold"></i> Master Voice
                    </button>
                </div>

                <!-- Speech Transcript Box -->
                <div id="train-transcript-box" class="bg-black/40 border border-dashed border-gray-600 rounded-xl p-4 max-w-2xl mx-auto mb-6 text-xs md:text-sm text-gray-400 min-h-[50px] flex items-center justify-center">
                    <span>Press microphone button and recite the full incantation...</span>
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
    <!-- MODAL FOR SPELL DETAILS (JP -> Romaji -> TH) -->
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
                    <p id="modal-thai-chant" class="text-base sm:text-lg text-gray-200 leading-relaxed font-light italic whitespace-pre-line">"..."</p>
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

    <!-- Engine API Settings Modal -->
    <div id="engine-settings-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-md" onclick="closeEngineSettings()"></div>
        <div class="modal-content relative w-full max-w-md rounded-2xl p-6 text-left z-10 border-2 border-magic-gold">
            <h3 class="font-cinzel text-xl font-bold text-magic-gold mb-1"><i class="fa-solid fa-gear mr-2"></i> Voice Engine Settings</h3>
            <p class="text-xs text-gray-400 mb-4">Configure AI Cloud API Keys for Method 2 (Serverless Whisper).</p>

            <div class="mb-4">
                <label class="block text-xs uppercase font-cinzel text-gray-300 mb-1">Groq API Key (Free & 300ms fast):</label>
                <input type="password" id="cfg-groq-key" placeholder="gsk_..." class="w-full bg-black/60 border border-magic-gold/30 rounded-lg p-2.5 text-xs text-white placeholder-gray-600 focus:outline-none focus:border-magic-gold">
                <p class="text-[11px] text-gray-500 mt-1">Get free key at <a href="https://console.groq.com/keys" target="_blank" class="text-magic-gold hover:underline">groq.com</a> (or set GROQ_API_KEY on Vercel).</p>
            </div>

            <div class="mb-5">
                <label class="block text-xs uppercase font-cinzel text-gray-300 mb-1">OpenAI API Key (Optional):</label>
                <input type="password" id="cfg-openai-key" placeholder="sk-..." class="w-full bg-black/60 border border-magic-gold/30 rounded-lg p-2.5 text-xs text-white placeholder-gray-600 focus:outline-none focus:border-magic-gold">
            </div>

            <div class="flex justify-end gap-3">
                <button onclick="closeEngineSettings()" class="px-4 py-2 rounded-lg bg-white/10 text-xs font-cinzel text-gray-300">Cancel</button>
                <button onclick="saveEngineSettings()" class="px-5 py-2 rounded-lg bg-magic-gold text-magic-dark font-cinzel font-bold text-xs">Save Settings</button>
            </div>
        </div>
    </div>

    <!-- ======================================================== -->
    <!-- JAVASCRIPT LOGIC -->
    <!-- ======================================================== -->
    <script>
        const spellsData = ''' + json.dumps(spells, ensure_ascii=False) + ''';

        // ENGINE CONFIGURATION
        let currentVoiceEngine = localStorage.getItem('mushoku_voice_engine') || 'stream';
        let customGroqKey = localStorage.getItem('mushoku_groq_key') || '';
        let customOpenaiKey = localStorage.getItem('mushoku_openai_key') || '';

        function setVoiceEngine(engine) {
            currentVoiceEngine = engine;
            localStorage.setItem('mushoku_voice_engine', engine);

            const btnStream = document.getElementById('engine-btn-stream');
            const btnCloud = document.getElementById('engine-btn-cloud');
            const btnBrowserAi = document.getElementById('engine-btn-browser_ai');

            [btnStream, btnCloud, btnBrowserAi].forEach(btn => {
                if (!btn) return;
                btn.className = "px-3 py-1.5 rounded-xl text-xs font-cinzel border border-white/10 bg-white/5 text-gray-300 hover:text-white transition-all";
            });

            const activeClass = "px-3 py-1.5 rounded-xl text-xs font-cinzel border border-magic-gold bg-magic-gold text-magic-dark font-bold transition-all shadow-[0_0_10px_rgba(197,160,89,0.3)]";

            if (engine === 'stream' && btnStream) btnStream.className = activeClass;
            if (engine === 'cloud' && btnCloud) btnCloud.className = activeClass;
            if (engine === 'browser_ai' && btnBrowserAi) {
                btnBrowserAi.className = activeClass;
                preloadBrowserAiModel();
            }

            const box = document.getElementById('train-transcript-box');
            if (box) {
                if (engine === 'stream') box.innerHTML = `<span><i class="fa-solid fa-bolt mr-2 text-magic-gold"></i>Live Web Speech: Recite the full incantation into the microphone.</span>`;
                else if (engine === 'cloud') box.innerHTML = `<span><i class="fa-solid fa-cloud mr-2 text-cyan-400"></i>Cloud Whisper: Record the full audio and send for AI evaluation.</span>`;
                else if (engine === 'browser_ai') box.innerHTML = `<span><i class="fa-solid fa-robot mr-2 text-purple-400"></i>Web AI: Client-side Whisper will transcribe 100% locally.</span>`;
            }
        }

        function openEngineSettings() {
            document.getElementById('cfg-groq-key').value = customGroqKey;
            document.getElementById('cfg-openai-key').value = customOpenaiKey;
            document.getElementById('engine-settings-modal').classList.remove('hidden');
        }

        function closeEngineSettings() {
            document.getElementById('engine-settings-modal').classList.add('hidden');
        }

        function saveEngineSettings() {
            customGroqKey = document.getElementById('cfg-groq-key').value.trim();
            customOpenaiKey = document.getElementById('cfg-openai-key').value.trim();
            localStorage.setItem('mushoku_groq_key', customGroqKey);
            localStorage.setItem('mushoku_openai_key', customOpenaiKey);
            closeEngineSettings();
            alert('Engine settings saved successfully!');
        }

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
                setVoiceEngine(currentVoiceEngine);
            } else if (tab === 'battle') {
                document.getElementById('view-battle').classList.remove('hidden');
                document.getElementById('tab-btn-battle').className = "px-6 py-2.5 rounded-full font-cinzel text-sm uppercase tracking-wider font-semibold transition-all border border-magic-gold bg-magic-gold text-magic-dark shadow-[0_0_15px_rgba(197,160,89,0.4)]";
            }
        }

        // =========================================================
        // 1. GRIMOIRE CARD RENDER (firstOne.html design)
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
        // 2. TRAINING MODE (FULL CHANT RECITATION - NO CHUNKING)
        // =========================================================
        let trainingQueue = [];
        let trainCurrentIndex = 0;
        let isTrainingRecording = false;
        let accumulatedLiveTranscript = '';

        // Audio Recorder State (for Cloud & Web AI)
        let mediaRecorder = null;
        let audioChunks = [];
        let browserAiTranscriber = null;
        let isModelLoading = false;

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
            document.getElementById('train-transcript-box').innerHTML = `<span>Press microphone button and recite the full incantation...</span>`;
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

        // =========================================================
        // SPEECH RECOGNITION (FULL CHANT EVALUATION)
        // =========================================================

        let recognition = null;
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRec();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'ja-JP';
        }

        function toggleTrainingSpeech() {
            if (currentVoiceEngine === 'stream') {
                toggleLiveStreamSpeech();
            } else if (currentVoiceEngine === 'cloud') {
                toggleCloudAiRecording();
            } else if (currentVoiceEngine === 'browser_ai') {
                toggleBrowserAiRecording();
            }
        }

        // ENGINE 1: LIVE WEB SPEECH (Full Chant Continuous Stream)
        function toggleLiveStreamSpeech() {
            if (!recognition) {
                const manual = prompt('Speech Recognition not supported in this browser. Enter chant transcript:');
                if (manual) evaluateFullChant(manual);
                return;
            }

            const micBtn = document.getElementById('train-mic-btn');
            const box = document.getElementById('train-transcript-box');

            if (isTrainingRecording) {
                // User clicked to finish chanting
                isTrainingRecording = false;
                recognition.stop();
                micBtn.classList.remove('recording-pulse');
                if (accumulatedLiveTranscript.trim()) {
                    evaluateFullChant(accumulatedLiveTranscript);
                } else {
                    box.innerHTML = `<span>Session ended. No speech detected.</span>`;
                }
            } else {
                accumulatedLiveTranscript = '';
                recognition.start();
                isTrainingRecording = true;
                micBtn.classList.add('recording-pulse');
                box.innerHTML = `<span class="text-magic-gold animate-pulse"><i class="fa-solid fa-ear-listen mr-2"></i>Listening to full chant... Recite now, and click mic when finished!</span>`;

                recognition.onresult = (e) => {
                    let interim = '';
                    for (let i = e.resultIndex; i < e.results.length; ++i) {
                        interim += e.results[i][0].transcript;
                        if (e.results[i].isFinal) {
                            accumulatedLiveTranscript += ' ' + e.results[i][0].transcript;
                        }
                    }
                    const liveHeard = accumulatedLiveTranscript + ' ' + interim;
                    box.innerHTML = `<span class="text-white">Heard: "${liveHeard.trim()}"</span>`;

                    // Check if final spell trigger was spoken (auto-complete)
                    const s = trainingQueue[trainCurrentIndex];
                    if (s) {
                        const finalTrigger = (s.jp_name || s.en).replace(/[「」『』、。・\\s!?]/g, '').toLowerCase();
                        const cleanLive = liveHeard.replace(/[「」『』、。・\\s!?]/g, '').toLowerCase();
                        if (cleanLive.includes(finalTrigger) && cleanLive.length >= 8) {
                            // Automatically evaluate when spell trigger is spoken
                            setTimeout(() => {
                                if (isTrainingRecording) {
                                    isTrainingRecording = false;
                                    recognition.stop();
                                    micBtn.classList.remove('recording-pulse');
                                    evaluateFullChant(liveHeard);
                                }
                            }, 500);
                        }
                    }
                };

                recognition.onerror = (err) => {
                    isTrainingRecording = false;
                    micBtn.classList.remove('recording-pulse');
                    box.innerHTML = `<span class="text-red-400">Mic notice: ${err.error || 'stopped'}. Click mic to restart.</span>`;
                };

                recognition.onend = () => {
                    if (isTrainingRecording) {
                        try { recognition.start(); } catch(e) {}
                    } else {
                        micBtn.classList.remove('recording-pulse');
                    }
                };
            }
        }

        // ENGINE 2: SERVERLESS CLOUD AI (Groq / OpenAI Whisper)
        async function toggleCloudAiRecording() {
            const micBtn = document.getElementById('train-mic-btn');
            const box = document.getElementById('train-transcript-box');

            if (isTrainingRecording) {
                isTrainingRecording = false;
                micBtn.classList.remove('recording-pulse');
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                }
            } else {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];

                    mediaRecorder.ondataavailable = (e) => {
                        if (e.data.size > 0) audioChunks.push(e.data);
                    };

                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                        box.innerHTML = `<span class="text-cyan-400 animate-pulse"><i class="fa-solid fa-cloud-arrow-up mr-2"></i>Sending full chant to Serverless Whisper AI...</span>`;
                        await sendAudioToServerlessWhisper(audioBlob);
                        stream.getTracks().forEach(t => t.stop());
                    };

                    mediaRecorder.start();
                    isTrainingRecording = true;
                    micBtn.classList.add('recording-pulse');
                    box.innerHTML = `<span class="text-cyan-400 animate-pulse"><i class="fa-solid fa-microphone mr-2"></i>[Cloud AI] Recording full chant... Recite completely and click mic to evaluate!</span>`;
                } catch (err) {
                    box.innerHTML = `<span class="text-red-400">Microphone access denied: ${err.message}</span>`;
                }
            }
        }

        async function sendAudioToServerlessWhisper(blob) {
            const s = trainingQueue[trainCurrentIndex];
            const box = document.getElementById('train-transcript-box');

            try {
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = async () => {
                    const base64Audio = reader.result.split(',')[1];
                    let endpoint = '/api/transcribe';
                    let headers = {
                        'Content-Type': 'application/json',
                        'x-target-spell': s.en
                    };
                    if (customGroqKey) headers['x-api-key'] = customGroqKey;
                    else if (customOpenaiKey) headers['x-api-key'] = customOpenaiKey;

                    const res = await fetch(endpoint, {
                        method: 'POST',
                        headers: headers,
                        body: JSON.stringify({ audio: base64Audio })
                    });

                    if (!res.ok) {
                        const err = await res.json().catch(() => ({}));
                        box.innerHTML = `<span class="text-yellow-400">Cloud API notice: ${err.error || 'Serverless endpoint unavailable'}. Check API key in settings.</span>`;
                        return;
                    }

                    const data = await res.json();
                    const transcript = data.text || '';
                    box.innerHTML = `<span class="text-white">AI Heard: "${transcript}"</span>`;
                    evaluateFullChant(transcript);
                };
            } catch (err) {
                box.innerHTML = `<span class="text-red-400">Error connecting to Whisper API: ${err.message}</span>`;
            }
        }

        // ENGINE 3: CLIENT-SIDE WEB AI (Transformers.js Whisper-tiny)
        async function preloadBrowserAiModel() {
            if (browserAiTranscriber || isModelLoading) return;
            const loadBox = document.getElementById('model-loading-box');
            const loadBar = document.getElementById('model-loading-bar');
            const loadPercent = document.getElementById('model-loading-percent');

            if (!window.transformersPipeline) {
                setTimeout(preloadBrowserAiModel, 500);
                return;
            }

            try {
                isModelLoading = true;
                if (loadBox) loadBox.classList.remove('hidden');

                browserAiTranscriber = await window.transformersPipeline('automatic-speech-recognition', 'Xenova/whisper-tiny', {
                    progress_callback: (p) => {
                        if (p.status === 'progress' && loadBar) {
                            const pct = Math.round(p.progress || 0);
                            loadBar.style.width = pct + '%';
                            if (loadPercent) loadPercent.textContent = pct + '%';
                        }
                    }
                });

                if (loadBox) {
                    loadBox.classList.add('hidden');
                    alert('Web AI Whisper model loaded into browser cache successfully! 100% offline ready.');
                }
            } catch (err) {
                if (loadBox) loadBox.classList.add('hidden');
                console.warn('Web AI load error:', err);
            } finally {
                isModelLoading = false;
            }
        }

        async function toggleBrowserAiRecording() {
            const micBtn = document.getElementById('train-mic-btn');
            const box = document.getElementById('train-transcript-box');

            if (isTrainingRecording) {
                isTrainingRecording = false;
                micBtn.classList.remove('recording-pulse');
                if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
            } else {
                if (!browserAiTranscriber) {
                    await preloadBrowserAiModel();
                }

                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];

                    mediaRecorder.ondataavailable = (e) => {
                        if (e.data.size > 0) audioChunks.push(e.data);
                    };

                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                        box.innerHTML = `<span class="text-purple-400 animate-pulse"><i class="fa-solid fa-microchip mr-2"></i>Transcribing full chant locally with Web AI Whisper...</span>`;
                        await runLocalWhisperTranscribe(audioBlob);
                        stream.getTracks().forEach(t => t.stop());
                    };

                    mediaRecorder.start();
                    isTrainingRecording = true;
                    micBtn.classList.add('recording-pulse');
                    box.innerHTML = `<span class="text-purple-400 animate-pulse"><i class="fa-solid fa-microphone mr-2"></i>[Web AI] Recording full chant... Recite completely and click mic to evaluate!</span>`;
                } catch (err) {
                    box.innerHTML = `<span class="text-red-400">Microphone error: ${err.message}</span>`;
                }
            }
        }

        async function runLocalWhisperTranscribe(blob) {
            const box = document.getElementById('train-transcript-box');
            try {
                const arrayBuffer = await blob.arrayBuffer();
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
                const decoded = await audioCtx.decodeAudioData(arrayBuffer);
                const float32Data = decoded.getChannelData(0);

                const out = await browserAiTranscriber(float32Data, {
                    language: 'japanese',
                    task: 'transcribe'
                });

                const transcript = out.text || '';
                box.innerHTML = `<span class="text-white">Local AI Heard: "${transcript}"</span>`;
                evaluateFullChant(transcript);
            } catch (err) {
                box.innerHTML = `<span class="text-red-400">Web AI processing error: ${err.message}</span>`;
            }
        }

        // UNIFIED FULL-CHANT ACCURACY EVALUATION (NO SYLLABLE BREAKDOWN)
        function evaluateFullChant(spoken) {
            const spell = trainingQueue[trainCurrentIndex];
            const cleanSpoken = spoken.replace(/[「」『』、。・\\s!?]/g, '').toLowerCase();
            const cleanTargetJp = spell.jp.replace(/[「」『』、。・\\s!?]/g, '').toLowerCase();
            const cleanTargetRomaji = spell.romaji.replace(/[,.!?\\s"'–—]/g, '').toLowerCase();
            const spellTrigger = (spell.jp_name || spell.en).replace(/[「」『』、。・\\s!?]/g, '').toLowerCase();

            // Check anchor keywords across the incantation
            const anchors = [
                '水の精霊', '水', '雷帝', '神なる力', '神', '灯火', '炎', '大地', '王女', 'せせらぎ',
                '加護', '求める所', '慈愛', '女神', '氷霜', '鎧', '鎧を纏わん', '押し流せ', '熱さ',
                spell.en.toLowerCase(),
                spellTrigger
            ];

            let anchorMatches = 0;
            anchors.forEach(a => {
                if (cleanTargetJp.includes(a.toLowerCase()) && cleanSpoken.includes(a.toLowerCase())) {
                    anchorMatches++;
                }
            });

            // Character overlap ratio
            let charMatches = 0;
            for (const ch of cleanSpoken) {
                if (cleanTargetJp.includes(ch)) charMatches++;
            }
            const ratio = cleanTargetJp.length > 0 ? (charMatches / cleanTargetJp.length) : 0;
            const hasTrigger = cleanSpoken.includes(spellTrigger) || cleanSpoken.includes(spell.en.toLowerCase());

            const badge = document.getElementById('train-result-badge');

            if (ratio >= 0.55 || (anchorMatches >= 2 && hasTrigger) || ratio >= 0.40 && hasTrigger) {
                badge.innerHTML = `
                    <div class="inline-block px-5 py-2.5 rounded-full bg-green-500/20 border-2 border-green-500 text-green-300 font-cinzel text-sm shadow-[0_0_20px_rgba(16,185,129,0.4)]">
                        <i class="fa-solid fa-circle-check mr-2 text-green-400"></i> S-RANK: PERFECT INCANTATION COMPLETED! (${Math.min(100, Math.round(ratio * 100) + 20)}%)
                    </div>
                `;
            } else if (hasTrigger || anchorMatches >= 1 || ratio >= 0.25) {
                badge.innerHTML = `
                    <div class="inline-block px-5 py-2.5 rounded-full bg-yellow-500/20 border border-yellow-500 text-yellow-300 font-cinzel text-sm">
                        <i class="fa-solid fa-triangle-exclamation mr-2 text-yellow-400"></i> A-RANK / PASS: ACCENT TOLERATED (Spell Success)
                    </div>
                `;
            } else {
                badge.innerHTML = `
                    <div class="inline-block px-4 py-2 rounded-full bg-red-500/20 border border-red-500 text-red-300 font-cinzel text-sm">
                        <i class="fa-solid fa-circle-xmark mr-2 text-red-400"></i> B-RANK: Incantation incomplete. Please chant the full words and spell trigger!
                    </div>
                `;
            }
        }

        // =========================================================
        // 3. BALANCED SPELL BATTLE RPG
        // =========================================================
        const enemies = {
            crawler: { name: 'Iron Crawler', type: 'Beast', maxHp: 750, hp: 750, atk: 45, def: 'heavy', weak: ['Ice', 'Lightning'], strong: ['Fire'] },
            treant: { name: 'Forest Treant', type: 'Plant', maxHp: 900, hp: 900, atk: 55, def: 'wood', weak: ['Fire'], strong: ['Water', 'Earth'] },
            salamander: { name: 'Magma Salamander', type: 'Elemental', maxHp: 800, hp: 800, atk: 65, def: 'heat', weak: ['Water', 'Ice'], strong: ['Fire'] },
            wyvern: { name: 'Red Wyvern', type: 'Dragonkin', maxHp: 1200, hp: 1200, atk: 85, def: 'flying', weak: ['Cumulonimbus', 'Dragon', 'Lightning'], strong: ['Earth'] }
        };

        let combat = {
            playerHp: 500,
            playerMaxHp: 500,
            playerMp: 350,
            playerMaxMp: 350,
            turn: 1,
            enemyKey: 'crawler',
            enemy: null,
            comboWet: false,
            comboDefDown: false,
            pendingSpell: null
        };

        function initBattle() {
            const eKey = document.getElementById('battle-enemy-select').value;
            combat.enemyKey = eKey;
            combat.enemy = JSON.parse(JSON.stringify(enemies[eKey]));
            combat.playerHp = combat.playerMaxHp;
            combat.playerMp = combat.playerMaxMp;
            combat.turn = 1;
            combat.comboWet = false;
            combat.comboDefDown = false;

            document.getElementById('enemy-name-text').innerHTML = `<i class="fa-solid fa-skull mr-2"></i>${combat.enemy.name}`;
            document.getElementById('enemy-weakness-text').textContent = `Weak: ${combat.enemy.weak.join(', ')}`;

            updateBattleUI();
            logBattle('[COMBAT SYSTEM] Enemy encountered! Choose a spell action below to chant.');
            populateBattleSlots();
        }

        function populateBattleSlots() {
            const container = document.getElementById('battle-slots-container');
            container.innerHTML = '';

            const battleSpellIds = [2, 8, 12, 16, 20, 21, 5, 1];
            const battleSpells = spellsData.filter(s => battleSpellIds.includes(s.id));

            battleSpells.forEach(s => {
                const canAfford = combat.playerMp >= s.mp_cost;
                const slotHtml = `
                    <div class="bg-black/50 border border-magic-gold/30 hover:border-magic-gold rounded-xl p-3 flex flex-col justify-between transition-all ${!canAfford ? 'opacity-40 pointer-events-none' : 'hover:scale-[1.02] cursor-pointer'}" onclick="prepareCastBattleSpell(${s.id})">
                        <div class="flex justify-between items-center mb-1">
                            <span class="text-xs font-bold text-white font-cinzel">${s.en}</span>
                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/20 text-cyan-300 font-cinzel">${s.mp_cost} MP</span>
                        </div>
                        <div class="text-[11px] text-magic-gold-light italic mb-2">${s.romaji_name}</div>
                        <div class="text-[10px] text-gray-400 mt-auto flex justify-between">
                            <span>PWR: ${s.power}</span>
                            <span class="text-magic-gold">${s.element}</span>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', slotHtml);
            });
        }

        function prepareCastBattleSpell(spellId) {
            const spell = spellsData.find(s => s.id === spellId);
            if (!spell) return;
            combat.pendingSpell = spell;

            document.getElementById('battle-chant-spell-name').textContent = spell.en;
            document.getElementById('battle-chant-jp').textContent = `「${spell.jp}」`;
            document.getElementById('battle-chant-romaji').textContent = spell.romaji;
            document.getElementById('battle-transcript-text').textContent = 'Press mic and chant to cast, or click Fast Cast!';

            document.getElementById('battle-chant-modal').classList.remove('hidden');
        }

        function closeBattleChantModal() {
            document.getElementById('battle-chant-modal').classList.add('hidden');
            combat.pendingSpell = null;
        }

        function instantCastBattleSpell() {
            if (!combat.pendingSpell) return;
            executeBattleSpell(combat.pendingSpell);
            closeBattleChantModal();
        }

        function toggleBattleSpeech() {
            if (combat.pendingSpell) {
                instantCastBattleSpell();
            }
        }

        function executeBattleSpell(spell) {
            combat.playerMp = Math.max(0, combat.playerMp - spell.mp_cost);

            if (spell.type === 'heal') {
                const healAmt = spell.power * 2;
                combat.playerHp = Math.min(combat.playerMaxHp, combat.playerHp + healAmt);
                logBattle(`[CAST] You chanted ${spell.en}! Restored ${healAmt} HP.`);
            } else {
                let dmg = spell.power;
                let multiplier = 1.0;

                // Elemental Weakness
                if (combat.enemy.weak.includes(spell.element) || combat.enemy.weak.includes(spell.en)) {
                    multiplier += 0.5;
                    logBattle(`[WEAKNESS] ${combat.enemy.name} is weak against ${spell.element}! (1.5x Dmg)`);
                }

                // Combo System: Water Splash + Ice = Freeze Shatter!
                if (spell.en === 'Water Splash') {
                    combat.comboWet = true;
                    logBattle(`[COMBO READY] Target is drenched in water! Follow with Ice to Shatter!`);
                } else if (combat.comboWet && (spell.en.includes('Ice') || spell.element === 'Water')) {
                    multiplier += 0.8;
                    combat.comboWet = false;
                    logBattle(`[FROST COMBO] SHATTER! Drenched foe frozen and fractured! (+80% Dmg)`);
                }

                const totalDmg = Math.round(dmg * multiplier);
                combat.enemy.hp = Math.max(0, combat.enemy.hp - totalDmg);
                logBattle(`[DAMAGE] You hit ${combat.enemy.name} for ${totalDmg} damage!`);
            }

            updateBattleUI();

            if (combat.enemy.hp <= 0) {
                logBattle(`[VICTORY] You defeated ${combat.enemy.name}! Final Grade: S-RANK MAGUS!`);
                alert(`Victory! ${combat.enemy.name} has fallen. Final Grade: S`);
                initBattle();
                return;
            }

            // Enemy Turn
            setTimeout(() => {
                enemyTurnAction();
            }, 800);
        }

        function enemyTurnAction() {
            combat.turn++;
            const dmg = combat.enemy.atk + Math.floor(Math.random() * 15);
            combat.playerHp = Math.max(0, combat.playerHp - dmg);
            logBattle(`[ENEMY] ${combat.enemy.name} attacks you for ${dmg} physical damage!`);

            combat.playerMp = Math.min(combat.playerMaxMp, combat.playerMp + 15);

            updateBattleUI();
            populateBattleSlots();

            if (combat.playerHp <= 0) {
                logBattle(`[DEFEAT] Rudeus has fallen. Grade: F`);
                alert('You were defeated in the labyrinth! Regroup and try again.');
                initBattle();
            }
        }

        function updateBattleUI() {
            document.getElementById('player-hp-text').textContent = `${combat.playerHp} / ${combat.playerMaxHp}`;
            document.getElementById('player-hp-bar').style.width = `${(combat.playerHp / combat.playerMaxHp) * 100}%`;

            document.getElementById('player-mp-text').textContent = `${combat.playerMp} / ${combat.playerMaxMp}`;
            document.getElementById('player-mp-bar').style.width = `${(combat.playerMp / combat.playerMaxMp) * 100}%`;

            if (combat.enemy) {
                document.getElementById('enemy-hp-text').textContent = `${combat.enemy.hp} / ${combat.enemy.maxHp}`;
                document.getElementById('enemy-hp-bar').style.width = `${(combat.enemy.hp / combat.enemy.maxHp) * 100}%`;
            }

            document.getElementById('battle-turn-count').textContent = combat.turn;
        }

        function logBattle(msg) {
            const box = document.getElementById('battle-log-box');
            box.innerHTML += `<div>${msg}</div>`;
            box.scrollTop = box.scrollHeight;
        }

        function triggerQuickVoiceBattle() {
            alert('Quick Cast: Chant any spell name into the mic!');
            if (spellsData.length > 0) {
                prepareCastBattleSpell(spellsData[0].id);
            }
        }

        // =========================================================
        // UTILITIES: COPY, TTS, AMBIENT PARTICLES
        // =========================================================
        function copyText(text, label = 'Text') {
            navigator.clipboard.writeText(text).then(() => {
                alert(`${label} copied to clipboard!`);
            }).catch(() => {
                prompt('Copy text manually:', text);
            });
        }

        function playVoice(text) {
            if (!('speechSynthesis' in window)) {
                alert('Speech synthesis not supported in this browser.');
                return;
            }
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(text);
            u.lang = 'ja-JP';
            u.rate = 0.95;
            window.speechSynthesis.speak(u);
        }

        // AMBIENT PARTICLES
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = (Math.random() - 0.5) * 0.4;
                this.speedY = (Math.random() - 0.5) * 0.4;
                this.alpha = Math.random() * 0.6 + 0.2;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.x < 0) this.x = canvas.width;
                if (this.x > canvas.width) this.x = 0;
                if (this.y < 0) this.y = canvas.height;
                if (this.y > canvas.height) this.y = 0;
            }
            draw() {
                ctx.fillStyle = `rgba(197, 160, 89, ${this.alpha})`;
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

print('Generated index.html with transparent circular favicon and full-chant voice recognition!')
