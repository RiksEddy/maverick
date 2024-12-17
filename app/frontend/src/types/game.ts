export interface GameStatus {
    status?: string;
    score: number;
    sequence: string[];
    current_index: number;
    game_active: boolean;
    current_color: string | null;
  }