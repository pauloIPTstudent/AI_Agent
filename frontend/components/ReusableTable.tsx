"use client"
import React from 'react';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper 
} from '@mui/material';

/**
 * @param {Array} data - Lista de objetos para exibir
 * @param {Array} columns - Configuração das colunas [{ key, label }]
 * @param {Function} onRowClick - Função chamada ao clicar na linha
 */
export default function ReusableTable({ data, columns, onRowClick }) {
  return (
    <TableContainer 
      component={Paper} 
      sx={{ 
        borderRadius: '12px', 
        overflow: 'hidden',
        boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
        border: '1px solid #e5e7eb' 
      }}
    >
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {columns.map((col) => (
              <TableCell 
                key={col.key} 
                sx={{ 
                  backgroundColor: '#f8fafc', 
                  fontWeight: 'bold', 
                  color: '#475569',
                  borderBottom: '2px solid #e2e8f0'
                }}
              >
                {col.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow
              key={row.id || index}
              onClick={() => onRowClick && onRowClick(row)}
              sx={{ 
                cursor: onRowClick ? 'pointer' : 'default',
                '&:hover': { backgroundColor: '#f1f5f9' },
                transition: 'background-color 0.2s ease'
              }}
            >
              {columns.map((col) => (
                <TableCell 
                  key={col.key}
                  sx={{ 
                    color: '#1e293b',
                    fontFamily: col.key === 'timestamp' ? 'monospace' : 'inherit' 
                  }}
                >
                  {row[col.key]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}