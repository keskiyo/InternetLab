import type { z } from 'zod';

import type { contactSchema } from '@/lib/schema';

/** Form values inferred from the Zod contact schema. */
export type ContactFormValues = z.infer<typeof contactSchema>;
