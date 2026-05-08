import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50 text-gray-900">
          {/* Header/Nav will go here */}
          <main className="p-8">
            <h1 className="text-3xl font-bold mb-4">InstaBot Dashboard</h1>
            <Routes>
              {/* Add routes here: Dashboard, Inbox, Orders, Leads */}
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
