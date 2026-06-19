export type Sentiment = 'positive' | 'negative' | 'neutral';
export type Category = 'frontend' | 'backend' | 'design' | 'consulting';
export type AIStatus = 'success' | 'fallback';

export interface ContactPayload {
  name: string;
  phone: string;
  email: string;
  comment: string;
}

export interface AIAnalysis {
  sentiment: Sentiment;
  category: Category;
  draft_reply: string;
  status: AIStatus;
}

export interface ContactResponse {
  id: number;
  name: string;
  email: string;
  created_at: string;
  ai: AIAnalysis;
  message: string;
}

/** Finite state for the contact form submission lifecycle. */
export type FormStatus = 'idle' | 'loading' | 'success' | 'error';
