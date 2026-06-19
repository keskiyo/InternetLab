import { forwardRef } from 'react'

import { cn } from '@/lib/cn'
import type { InputProps } from '@/types'

export const Input = forwardRef<HTMLInputElement, InputProps>(
	({ label, error, required, id, className, ...rest }, ref) => {
		const inputId = id ?? rest.name
		const errorId = error ? `${inputId}-error` : undefined
		return (
			<div className='flex flex-col gap-1.5'>
				<label
					htmlFor={inputId}
					className='text-sm font-medium text-fg'
				>
					{label}
					{required && <span className='ml-0.5 text-accent'>*</span>}
				</label>
				<input
					ref={ref}
					id={inputId}
					aria-invalid={error ? true : undefined}
					aria-describedby={errorId}
					className={cn(
						'bg-surface-muted border-app min-h-[44px] rounded-xl border px-4 py-2.5 text-sm text-fg',
						'placeholder:text-fg-muted/60 transition-colors duration-200',
						'focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/40',
						error &&
							'border-red-500 focus:border-red-500 focus:ring-red-500/30',
						className,
					)}
					{...rest}
				/>
				{error && (
					<p
						id={errorId}
						role='alert'
						className='text-xs text-red-500'
					>
						{error}
					</p>
				)}
			</div>
		)
	},
)

Input.displayName = 'Input'
