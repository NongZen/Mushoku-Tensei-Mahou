export interface Spell {
  id: number;
  name: string;
  en: string;
  jp: string;
  romaji: string;
  th: string;
  element: string;
  element_th?: string;
  tier: string;
  rank: string;
  rank_th?: string;
  mp_cost: number;
  power: number;
  type: string;
  effect: string;
  condition: string;
  casters: string[];
  jp_name: string;
  romaji_name: string;
  chunks_jp?: string[];
  chunks_romaji?: string[];
  sword_school?: 'Sword God' | 'Water God' | 'North God';
  sword_school_th?: string;
}

export type TabType = 'grimoire' | 'sword' | 'training' | 'battle';

export interface Enemy {
  name: string;
  type: string;
  maxHp: number;
  hp: number;
  atk: number;
  def: string;
  weak: string[];
  strong: string[];
  desc?: string;
}

export interface BattleState {
  playerHp: number;
  playerMaxHp: number;
  playerMp: number;
  playerMaxMp: number;
  turn: number;
  enemyKey: string;
  enemy: Enemy;
  comboWet: boolean;
  comboDefDown: boolean;
}
