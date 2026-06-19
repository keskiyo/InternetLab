import { cn } from '@/lib/cn'
import type { SpinnerProps } from '@/types'

export function Spinner({ className }: SpinnerProps): JSX.Element {
	return (
		<span
			role='status'
			aria-label='Загрузка'
			className={cn(
				'inline-block h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent',
				className,
			)}
		/>
	)
}
