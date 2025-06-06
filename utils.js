import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Combines multiple class names with Tailwind CSS support
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

/**
 * Formats a number as currency
 */
export function formatCurrency(value, currency = 'USD', locale = 'en-US') {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  }).format(value);
}

/**
 * Formats a number as percentage
 */
export function formatPercent(value, decimals = 2, locale = 'en-US') {
  return new Intl.NumberFormat(locale, {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value / 100);
}

/**
 * Truncates text to a specified length
 */
export function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
}

