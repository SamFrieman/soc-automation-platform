import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Typography,
  CircularProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Visibility, CheckCircle } from '@mui/icons-material';
import { alerts } from '../api/client';

function AlertsList() {
  const [alertsList, setAlertsList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [detailsOpen, setDetailsOpen] = useState(false);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await alerts.list();
      const data = response.data.results || response.data;
      setAlertsList(Array.isArray(data) ? data : []);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch alerts:', err);
      setError('Failed to load alerts');
      setLoading(false);
    }
  };

  const handleResolve = async (alertId) => {
    try {
      await alerts.resolve(alertId);
      fetchAlerts();
    } catch (err) {
      console.error('Failed to resolve alert:', err);
      alert('Failed to resolve alert');
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      CRITICAL: 'error',
      HIGH: 'warning',
      MEDIUM: 'info',
      LOW: 'success',
      INFO: 'default',
    };
    return colors[severity] || 'default';
  };

  const getStatusColor = (status) => {
    const colors = {
      NEW: 'error',
      INVESTIGATING: 'warning',
      IN_PROGRESS: 'info',
      RESOLVED: 'success',
      FALSE_POSITIVE: 'default',
    };
    return colors[status] || 'default';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Security Alerts
      </Typography>

      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Alert ID</strong></TableCell>
              <TableCell><strong>Title</strong></TableCell>
              <TableCell><strong>Severity</strong></TableCell>
              <TableCell><strong>Status</strong></TableCell>
              <TableCell><strong>Source IP</strong></TableCell>
              <TableCell><strong>Actions</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {alertsList.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Typography variant="body2" color="textSecondary">
                    No alerts found. Create some alerts to get started!
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              alertsList.map((alert) => (
                <TableRow key={alert.id} hover>
                  <TableCell>{alert.alert_id}</TableCell>
                  <TableCell>{alert.title}</TableCell>
                  <TableCell>
                    <Chip
                      label={alert.severity}
                      color={getSeverityColor(alert.severity)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={alert.status.replace('_', ' ')}
                      color={getStatusColor(alert.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{alert.source_ip || 'N/A'}</TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => {
                        setSelectedAlert(alert);
                        setDetailsOpen(true);
                      }}
                      title="View Details"
                    >
                      <Visibility />
                    </IconButton>
                    {alert.status !== 'RESOLVED' && (
                      <IconButton
                        size="small"
                        color="success"
                        onClick={() => handleResolve(alert.id)}
                        title="Resolve Alert"
                      >
                        <CheckCircle />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Alert Details Dialog */}
      <Dialog
        open={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Alert Details</DialogTitle>
        <DialogContent>
          {selectedAlert && (
            <Box>
              <Typography variant="h6" gutterBottom>{selectedAlert.title}</Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                {selectedAlert.description}
              </Typography>
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2"><strong>Alert ID:</strong> {selectedAlert.alert_id}</Typography>
                <Typography variant="subtitle2"><strong>Severity:</strong> {selectedAlert.severity}</Typography>
                <Typography variant="subtitle2"><strong>Status:</strong> {selectedAlert.status}</Typography>
                <Typography variant="subtitle2"><strong>Source IP:</strong> {selectedAlert.source_ip || 'N/A'}</Typography>
                <Typography variant="subtitle2"><strong>Affected User:</strong> {selectedAlert.affected_user || 'N/A'}</Typography>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default AlertsList;