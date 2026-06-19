import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  TextareaHTMLAttributes,
} from 'react';

import type { AIAnalysis, FormStatus } from './domain';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'ghost';
  loading?: boolean;
  children: ReactNode;
}

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export interface SpinnerProps {
  className?: string;
}

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  required?: boolean;
}

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
  required?: boolean;
}

export type BadgeTone = 'positive' | 'negative' | 'neutral' | 'accent';

export interface BadgeProps {
  tone?: BadgeTone;
  icon?: ReactNode;
  children: ReactNode;
}

export type ToastTone = 'success' | 'error';

export interface ToastProps {
  tone: ToastTone;
  message: string;
  onDismiss: () => void;
  /** Auto-dismiss delay in ms (default 4000). */
  duration?: number;
}

export interface AIStatusProps {
  status: FormStatus;
  ai: AIAnalysis | null;
}
