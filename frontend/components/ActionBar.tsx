"use client";

import React from 'react';

export default function ActionBar({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
       <div style={{paddingTop:18}}>
           {children}
       </div>
    </div>
  );
}
