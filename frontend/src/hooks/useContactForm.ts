import { zodResolver } from '@hookform/resolvers/zod'
import { useCallback, useState } from 'react'
import { useForm } from 'react-hook-form'

import { ApiError, submitContact } from '@/api/api'
import { contactSchema } from '@/lib/schema'
import type {
	AIAnalysis,
	ContactFormValues,
	FormStatus,
	UseContactFormReturn,
} from '@/types'

const DEFAULTS: ContactFormValues = {
	name: '',
	phone: '',
	email: '',
	comment: '',
}

export function useContactForm(): UseContactFormReturn {
	const form = useForm<ContactFormValues>({
		resolver: zodResolver(contactSchema),
		defaultValues: DEFAULTS,
		mode: 'onBlur',
	})

	const [status, setStatus] = useState<FormStatus>('idle')
	const [errorMessage, setErrorMessage] = useState<string | null>(null)
	const [ai, setAi] = useState<AIAnalysis | null>(null)

	const onSubmit = form.handleSubmit(async values => {
		setStatus('loading')
		setErrorMessage(null)
		setAi(null)
		try {
			const result = await submitContact(values)
			setAi(result.ai)
			setStatus('success')
			form.reset(DEFAULTS)
		} catch (err) {
			const message =
				err instanceof ApiError
					? err.message
					: 'Не удалось отправить заявку. Попробуйте позже.'
			setErrorMessage(message)
			setStatus('error')
		}
	})

	const reset = useCallback(() => {
		setStatus('idle')
		setErrorMessage(null)
		setAi(null)
		form.reset(DEFAULTS)
	}, [form])

	return { form, status, errorMessage, ai, onSubmit, reset }
}
