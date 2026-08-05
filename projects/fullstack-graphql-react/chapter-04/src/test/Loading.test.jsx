import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Loading from '../components/Loading.jsx';

describe('Loading component', () => {
  it('renders a bouncer div', () => {
    const { container } = render(<Loading />);
    expect(container.querySelector('.bouncer')).toBeInTheDocument();
  });

  it('applies custom color and size as inline styles', () => {
    const { container } = render(<Loading color="red" size={60} />);
    const bouncer = container.querySelector('.bouncer');
    expect(bouncer.getAttribute('style')).toContain('color: red');
    expect(bouncer.getAttribute('style')).toContain('width: 60px');
    expect(bouncer.getAttribute('style')).toContain('height: 60px');
  });
});
