import { CheckCircle2, X, XCircle } from 'lucide-react'
import { useEffect } from 'react'

import { cn } from '@/lib/cn'
import type { ToastProps } from '@/types'

export function Toast({
	tone,
	message,
	onDismiss,
	duration = 4000,
}: ToastProps): JSX.Element {
	useEffect(() => {
		const id = window.setTimeout(onDismiss, duration)
		return () => window.clearTimeout(id)
	}, [onDismiss, duration])

	const isSuccess = tone === 'success'

	return (
		<div
			role='status'
			aria-live='polite'
			className={cn(
				'fixed right-4 top-4 z-50 flex w-[min(92vw,400px)] items-start gap-3',
				'bg-surface border-app animate-fade-in rounded-xl border p-4 shadow-card',
			)}
		>
			{isSuccess ? (
				<CheckCircle2 className='mt-0.5 h-5 w-5 shrink-0 text-accent' />
			) : (
				<XCircle className='mt-0.5 h-5 w-5 shrink-0 text-red-500' />
			)}
			<p className='flex-1 text-sm text-fg'>{message}</p>
			<button
				type='button'
				onClick={onDismiss}
				aria-label='Закрыть уведомление'
				className='text-fg-muted hover:text-fg cursor-pointer transition-colors'
			>
				<X className='h-4 w-4' />
			</button>
		</div>
	)
}
