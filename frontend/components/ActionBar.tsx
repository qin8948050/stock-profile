"use client";

import React from 'react';

export default function ActionBar({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
      {children}
    </div>
  );
}
