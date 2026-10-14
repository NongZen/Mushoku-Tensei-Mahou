# 無職転生 魔術大全 — Mushoku Tensei Magic Grimoire (React + TypeScript)

เว็บแอปพลิเคชันรวบรวมบทร่ายและคำร่ายเวทมนตร์ฉบับสมบูรณ์จากนิยาย/อนิเมะ **เกิดชาตินี้พี่ต้องเป็นเทพ (Mushoku Tensei: Jobless Reincarnation)**
สร้างด้วย React 19, TypeScript, Tailwind CSS และ Vite พร้อมระบบ Grimoire Archive, Chanting Training Academy และ Turn-Based Spell Battle RPG

## คุณสมบัติเด่น (Features)
- 📖 **Grimoire Archive (คลังคาถาครบถ้วน)**:
  - บรรจุบทสวดเวทมนตร์ทั้ง 22 บท ตั้งแต่ระดับต้นไปจนถึงระดับศักดิ์สิทธิ์ ราชา และมังกรโบราณ
  - กรองตามธาตุ (น้ำ/น้ำแข็ง, ไฟ, ดิน, การรักษา/ศักดิ์สิทธิ์, มังกรโบราณ)
  - จัดเรียงตามธาตุและระดับขั้น, ลำดับขั้น (Tier/Level), หรือ ID ดั้งเดิม
  - ค้นหาแบบ Real-Time ทั้งชื่อเวทมนตร์ EN/TH/JP/Romaji และเนื้อหาคำร่าย
  - Grimoire Modal เจาะลึกบทสวด 3 ภาษา (Japanese, Romaji, Thai) พร้อมปุ่ม Copy และจำลองเสียงร่ายผ่าน Web Speech Synthesis

- 🎙️ **Chanting Academy (โหมดฝึกซ้อมร่ายเวท)**:
  - สุ่มคิวฝึกซ้อมร่ายเวทตามธาตุและระดับชั้นที่ต้องการ
  - รองรับ Live Web Speech Recognition สำหรับตรวจสอบความถูกต้องของคำร่าย
  - ระบบประเมินเกรด S-Rank, A-Rank (Pass) และ B-Rank ตามคำร่ายและคำกระตุ้นคาถา
  - รองรับการกรอกคำอ่านด้วยมือ (Manual Input) สำหรับกรณีอุปกรณ์ไม่รองรับไมโครโฟน

- ⚔️ **Labyrinth Battle Simulator (เกมประลองเวทมนตร์ RPG)**:
  - จำลองการต่อสู้ผลัดกันเล่น (Turn-Based Combat) กับสัตว์ประหลาดในวงกตเขาวงกต (Iron Crawler, Forest Treant, Magma Salamander, Red Wyvern)
  - จุดอ่อนธาตุ (Elemental Weaknesses 1.5x) และระบบ Combo ธาตุ (Water Splash + Ice = Frost Nova Shatter +80% Damage)
  - จัดการ HP และ MP คอยฟื้นฟูด้วยเวท Healing หรือฟื้นคืนมานาตามเทิร์น
  - รองรับการร่ายเวทผ่านไมโครโฟน หรือ Fast Cast (Skip Mic)

## การพัฒนาในเครื่อง (Local Development)
```bash
npm install
npm run dev
```

แอปจะเปิดบน `http://localhost:3000`
