import { Spell } from '../types';

export interface EvaluationResult {
  rank: 'S' | 'A' | 'B';
  message: string;
  scorePercent: number;
  matchedLanguage: 'jp' | 'th' | 'romaji';
}

function cleanText(str: string): string {
  return str.replace(/[「」『』'"“”‘’、。・\s!?.,()（）–—:;]/g, '').toLowerCase();
}

export function evaluateChant(spokenOrTyped: string, spell: Spell): EvaluationResult {
  const input = cleanText(spokenOrTyped);

  // 1. Thai Evaluation
  const cleanThTarget = cleanText(spell.th);
  const cleanThName = cleanText(spell.name.split('(')[0] || spell.name);

  const thaiAnchors = [
    cleanThName,
    'พลังแห่งทวยเทพ', 'กระแสธาร', 'พระผู้เป็นเจ้า', 'จักรพรรดิสายฟ้า',
    'ความกรุณา', 'ความเมตตา', 'เปลวเพลิง', 'ดาบน้ำแข็ง', 'เกราะพสุธา',
    'หยาดน้ำ', 'เทพธิดา', 'ราชาน้ำค้าง', 'แสงสว่าง', 'ดินเอ๋ย',
    'ภูตแสง', 'มังกร', 'ความภักดี', 'ดวงไฟ', 'คลื่นกระแสธาร', 'ทัณฑ์สวรรค์'
  ];

  let thaiAnchorMatches = 0;
  thaiAnchors.forEach((a) => {
    if (a && cleanThTarget.includes(a) && input.includes(a)) {
      thaiAnchorMatches++;
    }
  });

  let thCharMatches = 0;
  for (const ch of input) {
    if (cleanThTarget.includes(ch)) thCharMatches++;
  }
  const thRatio = cleanThTarget.length > 0 ? thCharMatches / cleanThTarget.length : 0;
  const thHasTrigger = cleanThName.length > 2 && input.includes(cleanThName);

  // 2. Japanese & Romaji Evaluation
  const cleanJpTarget = cleanText(spell.jp);
  const cleanRomajiTarget = cleanText(spell.romaji);
  const cleanJpName = cleanText(spell.jp_name || '');
  const cleanRomajiName = cleanText(spell.romaji_name || '');
  const cleanEn = cleanText(spell.en);

  const jpAnchors = [
    '水の精霊', '水', '雷帝', '神なる力', '神', '灯火', '炎', '大地', '王女', 'せせらぎ',
    '加護', '求める所', '慈愛', '女神', '氷霜', '鎧', '鎧を纏わん', '押し流せ', '熱さ',
    '光の精霊', '龍', '忠義', '後龍門', '前龍門', '救い', '治癒',
    cleanJpName, cleanRomajiName, cleanEn
  ];

  let jpAnchorMatches = 0;
  jpAnchors.forEach((a) => {
    if (a && cleanJpTarget.includes(a) && input.includes(a)) {
      jpAnchorMatches++;
    }
  });

  let jpCharMatches = 0;
  for (const ch of input) {
    if (cleanJpTarget.includes(ch) || cleanRomajiTarget.includes(ch)) jpCharMatches++;
  }
  const jpRatio = cleanJpTarget.length > 0 ? jpCharMatches / cleanJpTarget.length : 0;
  const jpHasTrigger =
    (cleanJpName.length > 1 && input.includes(cleanJpName)) ||
    (cleanRomajiName.length > 2 && input.includes(cleanRomajiName)) ||
    input.includes(cleanEn);

  // Determine best matched language score
  const isThaiScoreBetter =
    (thHasTrigger && !jpHasTrigger) ||
    (thRatio > jpRatio && thRatio > 0.15) ||
    (thaiAnchorMatches > jpAnchorMatches && thaiAnchorMatches > 0);

  if (isThaiScoreBetter) {
    const score = Math.min(100, Math.round(thRatio * 100) + (thHasTrigger ? 25 : 10));
    if (thRatio >= 0.45 || (thaiAnchorMatches >= 2 && thHasTrigger) || (thRatio >= 0.35 && thHasTrigger)) {
      return {
        rank: 'S',
        message: `S-RANK: PERFECT INCANTATION (THAI)! ยอดเยี่ยม บทร่ายภาษาไทยสมบูรณ์แบบ (${score}%)`,
        scorePercent: score,
        matchedLanguage: 'th',
      };
    } else if (thHasTrigger || thaiAnchorMatches >= 1 || thRatio >= 0.20) {
      return {
        rank: 'A',
        message: 'A-RANK / PASS (THAI): บทร่ายภาษาไทยผ่านเกณฑ์ เวทมนตร์สัมฤทธิ์ผล!',
        scorePercent: Math.max(score, 75),
        matchedLanguage: 'th',
      };
    } else {
      return {
        rank: 'B',
        message: 'B-RANK: บทร่ายยังไม่สมบูรณ์ กรุณาท่องหรือพิมพ์บทร่ายไทยและชื่อเวทให้ครบถ้วน!',
        scorePercent: Math.max(score, 40),
        matchedLanguage: 'th',
      };
    }
  } else {
    const score = Math.min(100, Math.round(jpRatio * 100) + (jpHasTrigger ? 25 : 10));
    if (jpRatio >= 0.45 || (jpAnchorMatches >= 2 && jpHasTrigger) || (jpRatio >= 0.35 && jpHasTrigger)) {
      return {
        rank: 'S',
        message: `S-RANK: PERFECT INCANTATION (JAPANESE)! 詠唱完了 (${score}%)`,
        scorePercent: score,
        matchedLanguage: 'jp',
      };
    } else if (jpHasTrigger || jpAnchorMatches >= 1 || jpRatio >= 0.20) {
      return {
        rank: 'A',
        message: 'A-RANK / PASS (JAPANESE): 呪文詠唱成功！(Accent Tolerated / Pass)',
        scorePercent: Math.max(score, 75),
        matchedLanguage: 'jp',
      };
    } else {
      return {
        rank: 'B',
        message: 'B-RANK: Incantation incomplete. Please chant or type the Japanese/Romaji incantation and spell name!',
        scorePercent: Math.max(score, 40),
        matchedLanguage: 'jp',
      };
    }
  }
}

/**
 * Matches a spoken or typed text to one of the available spells (in TH, JP, Romaji, or EN)
 */
export function findMatchingSpell(input: string, spells: Spell[]): Spell | null {
  const clean = cleanText(input);
  if (!clean || clean.length < 2) return null;

  // 1. Direct name match (highest priority)
  for (const s of spells) {
    const thClean = cleanText(s.name.split('(')[0]);
    const jpClean = cleanText(s.jp_name || '');
    const romajiClean = cleanText(s.romaji_name || '');
    const enClean = cleanText(s.en);

    if (
      clean === thClean ||
      clean === jpClean ||
      clean === romajiClean ||
      clean === enClean ||
      clean.includes(thClean) ||
      clean.includes(jpClean) ||
      clean.includes(enClean)
    ) {
      return s;
    }
  }

  // 2. Chant incantation substring match
  for (const s of spells) {
    const thChant = cleanText(s.th);
    const jpChant = cleanText(s.jp);
    const romajiChant = cleanText(s.romaji);

    if (
      (clean.length >= 4 && thChant.includes(clean)) ||
      (clean.length >= 4 && jpChant.includes(clean)) ||
      (clean.length >= 4 && romajiChant.includes(clean))
    ) {
      return s;
    }
  }

  return null;
}
