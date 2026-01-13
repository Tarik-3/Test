import { render, screen } from '@testing-library/react';
import App from './App';

test('renders DORA Metrics Demo heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/DORA Metrics Demo/i);
  expect(headingElement).toBeInTheDocument();
});

test('renders features list', () => {
  render(<App />);
  const springBootElement = screen.getByText(/Spring Boot Backend/i);
  expect(springBootElement).toBeInTheDocument();
});
