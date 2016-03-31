package com.programqii.printercontrol;

import android.content.DialogInterface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.programqii.printercontrol.services.GcodeCommandConstants;
import com.programqii.printercontrol.services.pojo.CommandRequest;
import com.programqii.printercontrol.services.pojo.CommandResponse;

import java.io.IOException;

import retrofit2.Response;

public class MainActivity extends BaseActivity {
	TextView positionTextView;
	EditText deltaEditText;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		positionTextView = (TextView)findViewById(R.id.positionTextView);
		new UpdatePositionTextTask().execute();

		Button printerHeadXDecButton = (Button)findViewById(R.id.printerHeadXDecButton);
		printerHeadXDecButton.setOnTouchListener(new View.OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				if(event.getAction() == MotionEvent.ACTION_DOWN) {
					new SendPositionCommandTask(GcodeCommandConstants.MOVE + " X-"+deltaEditText.getText()).execute();
				} else if (event.getAction() == MotionEvent.ACTION_UP) {
					//getGcodePrinterService().sendRawCommand(new CommandRequest());
				}
				return false;
			}
		});

		Button printerHeadXIncButton = (Button)findViewById(R.id.printerHeadXIncButton);
		printerHeadXIncButton.setOnTouchListener(new View.OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				if(event.getAction() == MotionEvent.ACTION_DOWN) {
					new SendPositionCommandTask(GcodeCommandConstants.MOVE + " X"+deltaEditText.getText()).execute();
				} else if (event.getAction() == MotionEvent.ACTION_UP) {
						//getGcodePrinterService().sendRawCommand(new CommandRequest());
				}
				return false;
			}
		});

		Button printerHeadYDecButton = (Button)findViewById(R.id.printerHeadYDecButton);
		printerHeadYDecButton.setOnTouchListener(new View.OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				if(event.getAction() == MotionEvent.ACTION_DOWN) {
					new SendPositionCommandTask(GcodeCommandConstants.MOVE + " Y-"+deltaEditText.getText()).execute();
				} else if (event.getAction() == MotionEvent.ACTION_UP) {
					//getGcodePrinterService().sendRawCommand(new CommandRequest());
				}
				return false;
			}
		});

		Button printerHeadYIncButton = (Button)findViewById(R.id.printerHeadYIncButton);
		printerHeadYIncButton.setOnTouchListener(new View.OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				if(event.getAction() == MotionEvent.ACTION_DOWN) {
					new SendPositionCommandTask(GcodeCommandConstants.MOVE + " Y"+deltaEditText.getText()).execute();
				} else if (event.getAction() == MotionEvent.ACTION_UP) {
					//getGcodePrinterService().sendRawCommand(new CommandRequest());
				}
				return false;
			}
		});

		Button printerHeadZDecButton = (Button)findViewById(R.id.printerHeadZDecButton);
		printerHeadZDecButton.setOnTouchListener(new View.OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				if(event.getAction() == MotionEvent.ACTION_DOWN) {
					new SendPositionCommandTask(GcodeCommandConstants.MOVE + " Z-"+deltaEditText.getText()).execute();
				} else if (event.getAction() == MotionEvent.ACTION_UP) {
					//getGcodePrinterService().sendRawCommand(new CommandRequest());
				}
				return false;
			}
		});

		Button printerHeadZIncButton = (Button)findViewById(R.id.printerHeadZIncButton);
		printerHeadZIncButton.setOnTouchListener(new View.OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				if(event.getAction() == MotionEvent.ACTION_DOWN) {
					new SendPositionCommandTask(GcodeCommandConstants.MOVE + " Z"+deltaEditText.getText()).execute();
				} else if (event.getAction() == MotionEvent.ACTION_UP) {
					//getGcodePrinterService().sendRawCommand(new CommandRequest());
				}
				return false;
			}
		});

		Button printerHomeButton = (Button)findViewById(R.id.printerHomeButton);
		printerHomeButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				new AlertDialog.Builder(MainActivity.this)
						.setTitle("Home Printer")
						.setMessage("Are you sure??")
						.setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
							public void onClick(DialogInterface dialog, int which) {
								// continue with delete
								new SendPositionCommandTask(GcodeCommandConstants.HOME).execute();
							}
						})
						.setNegativeButton(android.R.string.no, new DialogInterface.OnClickListener() {
							public void onClick(DialogInterface dialog, int which) {
								// do nothing
							}
						})
						.setIcon(android.R.drawable.ic_dialog_alert)
						.show();

			}
		});

		deltaEditText = (EditText)findViewById(R.id.deltaEditText);
	}
	public class SendPositionCommandTask extends AsyncTask<Void, Void, CommandResponse> {
		private String cmd;
		public SendPositionCommandTask(String cmd) {
			this.cmd = cmd;
		}
		@Override
		protected CommandResponse doInBackground(Void... params) {
			try {
				getGcodePrinterService().sendRawCommand(new CommandRequest(GcodeCommandConstants.SET_RELATIVE_COORDINATES)).execute();
				getGcodePrinterService().sendRawCommand(new CommandRequest(cmd)).execute();
				Response<CommandResponse> response = getGcodePrinterService().sendRawCommand(new CommandRequest(GcodeCommandConstants.GET_POSITION)).execute();
				return response.body();
			} catch (IOException e) {
				e.printStackTrace();
			}
			return null;
		}
		@Override
		protected void onPostExecute(CommandResponse response) {
			if(response != null && response.getData().size() > 0) {
				positionTextView.setText(response.getData().get(0));
			}
		}
	}
	public class UpdatePositionTextTask extends AsyncTask<Void, Void, CommandResponse> {

		@Override
		protected CommandResponse doInBackground(Void... params) {
			try {
				Response<CommandResponse> response = getGcodePrinterService().sendRawCommand(new CommandRequest(GcodeCommandConstants.GET_POSITION)).execute();
				return response.body();
			} catch (IOException e) {
				e.printStackTrace();
			}
			return null;
		}
		@Override
		protected void onPostExecute(CommandResponse response) {
			if(response != null && response.getData().size() > 0) {
				positionTextView.setText(response.getData().get(0));
			}
		}
	}
}
