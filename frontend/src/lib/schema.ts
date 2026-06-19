import { z } from 'zod';

/** Phone: digits, spaces, +, -, () — 7..20 chars. */
const phoneRegex = /^\+?[0-9\s\-()]{7,20}$/;

export const contactSchema = z.object({
  name: z
    .string()
    .trim()
    .min(2, 'Имя должно содержать минимум 2 символа')
    .max(120, 'Имя слишком длинное'),
  phone: z
    .string()
    .trim()
    .regex(phoneRegex, 'Введите корректный номер телефона'),
  email: z.string().trim().email('Введите корректный email'),
  comment: z
    .string()
    .trim()
    .min(5, 'Опишите задачу подробнее (минимум 5 символов)')
    .max(2000, 'Слишком длинный комментарий'),
});
