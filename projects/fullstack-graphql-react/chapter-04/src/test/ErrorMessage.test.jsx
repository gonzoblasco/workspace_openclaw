import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ErrorMessage from '../components/ErrorMessage.jsx';

describe('ErrorMessage component', () => {
  it('renders children inside error message div', () => {
    render(
      <ErrorMessage>
        <p>Something went wrong</p>
      </ErrorMessage>,
    );
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText('Something went wrong').closest('.error.message')).toBeInTheDocument();
  });
});
