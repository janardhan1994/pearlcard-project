// frontend/src/App.test.js

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import App from './App';

// Mock the entire axios library
jest.mock('axios');

describe('App Component', () => {

  beforeEach(() => {
    // Clear mock history before each test
    axios.get.mockClear();
  });

  test('should allow a user to add multiple journeys, see the total update, and delete them', async () => {
    // --- ARRANGE ---
    // For the initial config load
    axios.get.mockResolvedValueOnce({
      data: { available_zones: [1, 2, 3] },
    });

    render(<App />);
    const addButton = await screen.findByRole('button', { name: /add journey/i });
    const fromZoneSelect = screen.getByLabelText(/from zone/i);
    const toZoneSelect = screen.getByLabelText(/to zone/i);

    // --- ACT & ASSERT #1 (Add first journey) ---
    // Tell axios what to return for the NEXT .get() call
    axios.get.mockResolvedValueOnce({ data: { fare: 55 } });

    await userEvent.selectOptions(fromZoneSelect, '1');
    await userEvent.selectOptions(toZoneSelect, '2');
    await userEvent.click(addButton);

    expect(await screen.findByText(/trip 1: zone 1 → zone 2/i)).toBeInTheDocument();
    const totalFareValue1 = screen.getByText(/total daily fare/i).closest('.total-fare-container').querySelector('.total-value');
    expect(totalFareValue1).toHaveTextContent('55');

    // --- ACT & ASSERT #2 (Add second journey) ---
    // Tell axios what to return for the NEXT .get() call
    axios.get.mockResolvedValueOnce({ data: { fare: 30 } });
    
    await userEvent.selectOptions(fromZoneSelect, '3');
    await userEvent.selectOptions(toZoneSelect, '3');
    await userEvent.click(addButton);

    // Assert that the second journey appears and the total is updated
    expect(await screen.findByText(/trip 2: zone 3 → zone 3/i)).toBeInTheDocument();
    const totalFareValue2 = screen.getByText(/total daily fare/i).closest('.total-fare-container').querySelector('.total-value');
    expect(totalFareValue2).toHaveTextContent('85');

    // --- ACT & ASSERT #3 (Delete one journey) ---
    const deleteButtons = screen.getAllByTitle(/delete this journey/i);
    await userEvent.click(deleteButtons[0]);
    
    expect(screen.queryByText(/trip 1: zone 1 → zone 2/i)).not.toBeInTheDocument();
  });

  // The other tests are correct and do not need changes
  test('should display an error if adding a fare fails, without affecting existing journeys', async () => {
    axios.get.mockResolvedValueOnce({ data: { available_zones: [1, 2, 3] } });
    axios.get.mockResolvedValueOnce({ data: { fare: 40 } });
    render(<App />);
    const fromZoneSelect = await screen.findByLabelText(/from zone/i);
    await userEvent.selectOptions(fromZoneSelect, '1');
    await userEvent.click(screen.getByRole('button', { name: /add journey/i }));
    expect(await screen.findByText(/trip 1: zone 1 → zone 1/i)).toBeInTheDocument();
    axios.get.mockRejectedValueOnce(new Error('API Error'));
    await userEvent.selectOptions(fromZoneSelect, '2');
    await userEvent.click(screen.getByRole('button', { name: /add journey/i }));
    expect(await screen.findByText(/could not calculate fare for this journey/i)).toBeInTheDocument();
  });

  test('should display a loading error if the initial config call fails', async () => {
    axios.get.mockRejectedValueOnce(new Error('Config Load Error'));
    render(<App />);
    expect(await screen.findByText(/failed to load configuration from server/i)).toBeInTheDocument();
  });

  test('should clear all journeys when the reset button is clicked', async () => {
    axios.get.mockResolvedValueOnce({ data: { available_zones: [1, 2, 3] } });
    axios.get.mockResolvedValueOnce({ data: { fare: 55 } });
    render(<App />);
    const fromZoneSelect = await screen.findByLabelText(/from zone/i);
    await userEvent.selectOptions(fromZoneSelect, '1');
    await userEvent.click(screen.getByRole('button', { name: /add journey/i }));
    expect(await screen.findByText(/trip 1: zone 1 → zone 1/i)).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: /reset/i }));
    expect(screen.queryByText(/trip 1/i)).not.toBeInTheDocument();
  });
});