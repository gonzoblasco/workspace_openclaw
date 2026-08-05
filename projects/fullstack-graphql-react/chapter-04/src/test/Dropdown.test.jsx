import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Dropdown from '../components/Dropdown.jsx';

describe('Dropdown component', () => {
  it('shows content when trigger is clicked', () => {
    render(
      <Dropdown trigger={<button>Menu</button>}>
        <p>Dropdown content</p>
      </Dropdown>,
    );

    expect(screen.queryByText('Dropdown content')).not.toBeInTheDocument();

    fireEvent.click(screen.getByText('Menu'));
    expect(screen.getByText('Dropdown content')).toBeInTheDocument();
  });

  it('hides content when clicking outside', () => {
    render(
      <div>
        <Dropdown trigger={<button>Menu</button>}>
          <p>Dropdown content</p>
        </Dropdown>
        <div data-testid="outside">Outside</div>
      </div>,
    );

    fireEvent.click(screen.getByText('Menu'));
    expect(screen.getByText('Dropdown content')).toBeInTheDocument();

    fireEvent.mouseDown(screen.getByTestId('outside'));
    expect(screen.queryByText('Dropdown content')).not.toBeInTheDocument();
  });
});
