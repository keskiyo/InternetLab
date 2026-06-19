import { Send } from 'lucide-react'
import { useEffect, useState } from 'react'

import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Textarea } from '@/components/Textarea'
import { Toast } from '@/components/Toast'
import { useContactForm } from '@/hooks/useContactForm'
import { formatRuPhone } from '@/utils/phone'
import { AIStatus } from './AIStatus'

export function ContactForm(): JSX.Element {
	const { form, status, errorMessage, ai, onSubmit } = useContactForm()
	const {
		register,
		formState: { errors },
	} = form

	const [showToast, setShowToast] = useState(false)
	useEffect(() => {
		if (status === 'success' || status === 'error') setShowToast(true)
	}, [status])

	const phone = register('phone')

	return (
		<section id='contact' className='grid gap-6 lg:grid-cols-5'>
			<div className='lg:col-span-3'>
				<div className='bg-surface border-app rounded-xl border p-6 shadow-card sm:p-8'>
					<h2 className='font-heading mb-1 text-xl font-semibold text-fg'>
						Оставить заявку
					</h2>
					<p className='text-fg-muted mb-6 text-sm'>
						Опишите задачу.
					</p>

					<form onSubmit={onSubmit} noValidate className='space-y-4'>
						<div className='grid gap-4 sm:grid-cols-2'>
							<Input
								label='Имя'
								required
								autoComplete='name'
								placeholder='Иван Петров'
								error={errors.name?.message}
								{...register('name')}
							/>
							<Input
								label='Телефон'
								required
								type='tel'
								inputMode='tel'
								autoComplete='tel'
								maxLength={16}
								placeholder='+7 999 123-45-67'
								error={errors.phone?.message}
								{...phone}
								onChange={e => {
									e.target.value = formatRuPhone(
										e.target.value,
									)
									void phone.onChange(e)
								}}
							/>
						</div>
						<Input
							label='Email'
							required
							type='email'
							autoComplete='email'
							placeholder='ivan@example.com'
							error={errors.email?.message}
							{...register('email')}
						/>
						<Textarea
							label='Комментарий'
							required
							placeholder='Расскажите о проекте, сроках и бюджете…'
							error={errors.comment?.message}
							{...register('comment')}
						/>

						<Button
							type='submit'
							loading={status === 'loading'}
							className='w-full sm:w-auto'
						>
							{status === 'loading'
								? 'Отправляем…'
								: 'Отправить заявку'}
							{status !== 'loading' && (
								<Send className='h-4 w-4' />
							)}
						</Button>
					</form>
				</div>
			</div>

			<div className='lg:col-span-2'>
				<AIStatus status={status} ai={ai} />
			</div>

			{showToast && status === 'success' && (
				<Toast
					tone='success'
					message='Заявка отправлена! Я свяжусь с вами в ближайшее время.'
					onDismiss={() => setShowToast(false)}
				/>
			)}
			{showToast && status === 'error' && errorMessage && (
				<Toast
					tone='error'
					message={errorMessage}
					onDismiss={() => setShowToast(false)}
				/>
			)}
		</section>
	)
}
