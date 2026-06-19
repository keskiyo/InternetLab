import type { UseFormReturn } from 'react-hook-form';

import type { AIAnalysis, FormStatus } from './domain';
import type { ContactFormValues } from './forms';

export type Theme = 'light' | 'dark';

export interface UseThemeReturn {
  theme: Theme;
  toggleTheme: () => void;
}

export interface UseContactFormReturn {
  form: UseFormReturn<ContactFormValues>;
  status: FormStatus;
  errorMessage: string | null;
  ai: AIAnalysis | null;
  onSubmit: () => void;
  reset: () => void;
}
