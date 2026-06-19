import { Bot, Minus, Sparkles, Tag, ThumbsDown, ThumbsUp } from 'lucide-react'
import type { ReactNode } from 'react'

import { Badge } from '@/components/Badge'
import type { AIAnalysis, AIStatusProps, Sentiment } from '@/types'

const SENTIMENT_META: Record<
	Sentiment,
	{
		label: string
		tone: 'positive' | 'negative' | 'neutral'
		icon: ReactNode
	}
> = {
	positive: {
		label: 'Позитивная',
		tone: 'positive',
		icon: <ThumbsUp className='h-3.5 w-3.5' />,
	},
	negative: {
		label: 'Негативная',
		tone: 'negative',
		icon: <ThumbsDown className='h-3.5 w-3.5' />,
	},
	neutral: {
		label: 'Нейтральная',
		tone: 'neutral',
		icon: <Minus className='h-3.5 w-3.5' />,
	},
}

const CATEGORY_LABELS: Record<AIAnalysis['category'], string> = {
	frontend: 'Frontend',
	backend: 'Backend',
	design: 'Дизайн',
	consulting: 'Консультация',
}

function ShimmerLine({ w }: { w: string }): JSX.Element {
	return (
		<div
			className='bg-surface-muted relative overflow-hidden rounded-md'
			style={{ width: w, height: '0.85rem' }}
		>
			<div className='animate-shimmer absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent' />
		</div>
	)
}

export function AIStatus({ status, ai }: AIStatusProps): JSX.Element {
	return (
		<div className='border-app bg-surface rounded-xl border p-5'>
			<div className='mb-4 flex items-center gap-2'>
				<Bot className='h-5 w-5 text-accent' />
				<h3 className='font-heading text-sm font-semibold text-fg'>
					AI-анализ заявки
				</h3>
			</div>

			{status === 'idle' && (
				<p className='text-fg-muted text-sm leading-relaxed'>
					После отправки заявка автоматически анализируется YandexGPT:
					определяется тональность, категория и готовится черновик
					ответа.
				</p>
			)}

			{status === 'loading' && (
				<div className='space-y-3' aria-live='polite'>
					<div className='flex items-center gap-2 text-sm text-fg-muted'>
						<Sparkles className='h-4 w-4 animate-pulse text-accent' />
						Анализируем обращение…
					</div>
					<div className='space-y-2 pt-1'>
						<ShimmerLine w='55%' />
						<ShimmerLine w='90%' />
						<ShimmerLine w='75%' />
					</div>
				</div>
			)}

			{status === 'success' && ai && (
				<div className='animate-fade-in space-y-4'>
					<div className='flex flex-wrap gap-2'>
						<Badge
							tone={SENTIMENT_META[ai.sentiment].tone}
							icon={SENTIMENT_META[ai.sentiment].icon}
						>
							{SENTIMENT_META[ai.sentiment].label}
						</Badge>
						<Badge
							tone='accent'
							icon={<Tag className='h-3.5 w-3.5' />}
						>
							{CATEGORY_LABELS[ai.category]}
						</Badge>
						{ai.status === 'fallback' && (
							<Badge tone='neutral'>
								AI недоступен · черновик по умолчанию
							</Badge>
						)}
					</div>
					<div>
						<p className='text-fg-muted mb-1 text-xs font-medium uppercase tracking-wide'>
							Черновик ответа
						</p>
						<p className='bg-surface-muted rounded-xl p-4 text-sm leading-relaxed text-fg'>
							{ai.draft_reply}
						</p>
					</div>
				</div>
			)}

			{status === 'error' && (
				<p className='text-sm text-red-500'>
					Слишком много запросов, пожалуйста, повторите позже или
					обратитесь в службу поддержки.
				</p>
			)}
		</div>
	)
}
