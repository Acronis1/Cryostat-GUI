# coding=utf-8
# Commands for dealing with the LAKESHORE 350

import time, socket, threading, visa
import os, string
import numpy as np

from console_out import *

import logging

# create a logger object for this module
logger = logging.getLogger(__name__)
# added so that log messages show up in Jupyter notebooks
logger.addHandler(logging.StreamHandler())


class LAKESHORE350:
    def __init__(self):
        self.host = 'lakeshore'  # GPIB mnemonic for Lakeshore temp controller
        self.timeout = 30
        self.status = ''
        self.identity = ''
        self.connected = False
        self.selected_curve = ''
        self.style = '\033[7;95m'
        self.temp = ''
        self.text = Text()
        self.ComLock = threading.Lock()

    def connect(self):
        try:
            self.device = 'GPIB0::12:INSTR'
            self.identity = self.go('*IDN?')
            self.text.show(self.identity, 'message')
            self.status = 'connected'
            self.connected = True
            self.initialize()
            self.get_curves()

        except socket.timeout:
            self.status = "socket timeout"
            self.identity = 'none'
            self.connected = False
        return self.identity

    def initialize(self):
        """ Input Type Parameter Command
        INTYPE  <input>,
                <sensor type>, 3 = NTC RTD
                <autorange>, 1 = on
                <range>, 0 = 10ohm with NTC RTD
                <compensation>, 1 = on
                <units>, 1 = kelvin
                <sensor excitation> 0 = 1mV [term]

        """


        for a in ['A', 'B', 'C', 'D']:
            cmd = 'INTYPE %c,3,1,0,1,1,0' % (a)
            self.text.show(cmd, 'blue')
            self.ComLock.acquire()
            self.device.write(cmd + '\n')
            self.ComLock.release()



    def go(self, command): # writes command to device & shows received data
        self.ComLock.acquire()
        self.device.write(command)
        received = self.device.read(100).split('\r\n')[0]
        self.ComLock.release()
        self.text.show(command + '    ' + received[:10].strip() + '...', 'blue')
        return received.strip()


    def ClearInterfaceCommand(self):
        """Clear Interface Command
        Remarks:
            Clears the bits in the Status Register, Standard Event Status Register, and Operation Event Register,
            and terminates all pending operations. Clears the interface, but not the controller. The related
            controller command is *RST.
        """
        self.go('*CLS')

    def EventStatusEnableRegisterCommand(self, bit_weighting):
        """Event Status Enable Register Command
        Input:
            *ESE <bit weighting>[term]
        Format:
            nnn
        Remarks:
            Each bit is assigned a bit weighting and represents the enable/disable mask of the corresponding
            event flag bit in the Standard Event Status Register. To enable an event flag bit, send the
            command *ESE with the sum of the bit weighting for each desired bit.
            Refer to section 6.2.5 for a list of event flags.
        """
        self.go('*ESE ' + bit_weighting)

    def EventStatusEnableRegisterQuery(self):
        """Standard Event Status Enable Register Query
        Input:
            *ESE?[term]
        Returned:
            <bit weighting>[term]
        Format:
            nnn (Refer to section 6.2.5 for a list of event flags)
        """
        return self.go('*ESE?')

    def StandardEventStatusRegisterQuery(self):
        """Standard Event Status Register Query
        Input:
            *ESR?[term]
        Returned:
            <bit weighting>
        Format:
            nnn
        Remarks:
            The integer returned represents the sum of the bit weighting of the event flag bits in the
            Standard Event Status Register. Refer to section 6.2.5 for a list of event flags.
        """
        return self.go('*ESR?')

    def IdentificationQuery(self):
        """Identification Query
        Input:
            *IDN?[term]
        Returned:
            <manufacturer>,<model>,<instrument serial>/<option serial>,<firmware version>[term]
        Format:
            s[4],s[8],s[7]/s[7],n.n
        """
        return self.go('*IDN?')

    def OperationCompleteCommand(self):
        """Operation Complete Command
        Input:
            *OPC[term]
        Remarks:
            Generates an Operation Complete event in the Event Status Register upon
            completion of all pending selected device operations.
            Send it as the last command in a command string.
        """
        self.go('*OPC')

    def OperationCompleteQuery(self):
        """Operation Complete Query
        Input:
            *OPC?[term]
        Returned:
            1[term]
        Remarks:
            Places a 1 in the controller output queue upon completion of all pending selected device
            operations. Send as the last command in a command string. Not the same as *OPC.
        """
        self.go('*OPC?')

    def ResetInstrumentCommand(self):
        """Reset Instrument Command
        Input:
            *RST[term]
        Remarks:
            Sets controller parameters to power-up settings.
        """
        self.go('*RST')

    def ServiceRequestEnableRegisterCommand(self, bit_weighting):
        """Service Request Enable Register Command
        Input:
            *SRE <bit weighting>[term]
        Format:
            nnn
        Remarks:
            Each bit has a bit weighting and represents the enable/disable mask of the corresponding
            status flag bit in the Status Byte Register. To enable a status flag bit, send the command *SRE with
            the sum of the bit weighting for each desired bit. Refer to section 6.2.6 for a list of status flags.    
        """
        self.go('*SRE ' + bit_weighting)

    def ServiceRequestEnableRegisterQuery(self):
        """Service Request Enable Register Query
        Input:
            *SRE?[term]
        Returned:  
            <bit weighting>[term]
        Format:
            nnn (Refer to section 6.2.6 for a list of status flags)
        """
        self.go('*SRE?')

    def StatusByteQuery(self):
        """Status Byte Query
        Input:
            *STB?
        Returned:
            <bit weighting>[term]
        Format:
            nnn
        Remarks:
            Acts like a serial poll, but does not reset the register to all zeros. The integer returned
            represents the sum of the bit weighting of the status flag bits that are set in the Status Byte Register.
            Refer to section 6.2.6 for a list of status flags.
        """
        self.go('*STB?')

    def SelfTestQuery(self):
        """Self-Test Query
        Input:
            *TST?[term]
        Returned:
            <status>[term]
        Format:
            n
            <status>    0 = no errors found, 1 = errors found
        Remarks:
            The Model 350 reports status based on test done at power up.
        """
        return self.go('*TST?')

    def WaitToContinueCommand(self):
        """Wait-to-Continue Command
        Input:
            *WAI[term]
        Remarks:
            Causes the IEEE-488 interface to hold off until all pending operations have been completed.
            This is the same function as the *OPC command, except that it does not set the Operation Complete event
            bit in the Event Status Register.
        """
        self.go('*WAI*')

    def InputAlarmParameterCommand(self, command):
        """Input Alarm Parameter Command
        Input:
            ALARM <input>,<off/on>,<high value>,<low value>,<deadband>,<latch enable>,<audible>,<visible> [term]
        Format:
            a,n, ±nnnnnn, ±nnnnnn, +nnnnnn,n,n,n
            <input>         Specifies which input to configure: A - D (D1 - D5 for 3062 option).
            <off/on>        Determines whether the instrument checks the alarm for this input, where 0 = off and 1 = on.
            <high setpoint>  Sets the value the source is checked against to activate the high alarm.
            <low setpoint>  Sets the value the source is checked against to activate low alarm.
            <deadband>      Sets the value that the source must change outside of an alarm condition to deactivate an unlatched alarm.
            <latch enable>  Specifies a latched alarm (remains active after alarm condition correction) where 0 = off(no latch) and 1 = on.
            <audible>       Specifies if the internal speaker will beep when an alarm condition occurs. Valid entries: 0 = off, 1 = on.
            <visible>       Specifies if the Alarm LED on the instrument front panel will blink when an alarm condition occurs. Valid entries: 0 = off, 1 = on.
        """
        self.go('ALARM ' + command)

     def InputAlarmParameterQuery(self, command):
        """Input Alarm Parameter Query
        Input:
            ALARM? <input>[term]
        Format:
            a
            <input>         A - D (D1 - D5 for 3062 option)
        Returned:
            <off/on>,<high value>,<low value>,<deadband>,<latch enable>,<audible>,<visible> [term]
        Format:
            n,±nnnnnn,±nnnnnn,+nnnnnn,n,n,n (refer to command for description)
        """
        return self.go('ALARM? ' + command)

    def ResetAlarmStatusCommand(self):
        """Reset Alarm Status Command
        Input:
            ALMRST[term]
        Remarks:
            Clears both the high and low status of all alarms, including latching items.
        """
        self.go('ALMRST')

    def MonitorOutParameterCommand(self, command):
        """Monitor Out Parameter Command
        Input:
            ANALOG <output>,<input>,<units>,<high value>,<low value>,<polarity>[term]
        Format:
            n,n,n,±nnnnn,±nnnnn,n
            <output>        Unpowered analog output to configure: 3 or 4
            <input>         Specifies which input to monitor. 0 = none, 1 = Input A, 2 = Input B, 3 = Input C,
                            4 = Input D (5 = Input D2, 6 = Input D3, 7 = Input D4,8 = Input D5 for 3062 option)
            <units>         Specifies the units on which to base the output voltage: 1 = kelvin, 2 =  Celsius,
                            3 = sensor units
            <high value>    If output mode is Monitor Out, this parameter represents the data at which the
                            Monitor Out reaches +100% output.Entered in the units designated by the <units>
                               parameter. Refer to OUTMODE command.
            <low value>     If output mode is Monitor Out,this parameter represents the data at which the analog
                            output reaches -100% output if bipolar, or 0% output if positive only. Entered in the
                            units designated by the <units> parameter.
            <polarity>      Specifies output voltage is 0 = unipolar (positive output only) or bipolar (positive 
                            or negative output)
        Example:
            ANALOG 4,1,1,100.0,0.0,0[term] — sets output 4 to monitor Input A kelvin reading with 100.0 K at
            +100% output (+10.0 V) and 0.0 K at 0% output (0.0 V).
        Remarks:
            Use the OUTMODE command to set the output mode to Monitor Out. The <input> parameter in the ANALOG
            command is the same as the <input> parameter in the OUT- MODE command. It is included in the ANALOG command
            for backward compatibility with previous Lake Shore temperature monitors and controllers. The ANALOG com-
            mand name is also named as such for backward compatibility.
                
        """
        self.go('ANALOG ' + command)

    def MonitorOutParameterQuery(self, command):
        """Monitor Out Parameter Query
        Input:
            ANALOG? <output>[term]
        Format:
            n
            <output> Specifies which unpowered analog output to query the Monitor Out parameters for: 3 or 4.
        Returned:
            <input>,<units>,<high value>,<low value>,<polarity>[term]
        Format:
            n,n,±nnnnn,±nnnnn,n (refer to command for definition)
        """
        return self.go('ANALOG? ' + command)

    def AnalogOutputDataQuery(self, command):
        """Analog Output Data Query
        Input:
            AOUT? <output>[term]
        Format:
            n
            <output> Specifies which unpowered analog output to query: 3 or 4.
        Returned:
            <output percentage>[term]
        Format:
            ±nnn.n
        Remarks:
            Returns the output percentage of the unpowered analog output.
        """
        return self.go('AOUT? ' + command)

    def AutotuneCommand(self, command):
        """Autotune Command
        Input:
            ATUNE <output>,<mode>,[term]
        Format:
            n,n
            <output> Specifies the output associated with the loop to be Autotuned: 1–4.
            <mode> Specifies the Autotune mode. Valid entries: 0 = P Only, 1 = P and I, 2 = P, I, and D.
        Example:
            AT  UNE 2,1 [term]—initiates Autotuning of control loop associated with output 2, in P and I mode.
        Remarks:
            If initial conditions required to Autotune the specified loop are not met, an Autotune
            initialization error will occur and the Autotune process will not be performed. The TUNEST? query can be
            used to check if an Autotune error occurred.
        """
        self.go('ATUNE ' + command)

    def DisplayContrastCommand(self, command):
        """Display Contrast Command
        Input:
            BRIGT <contrast value>[term]
        Format:
            nn
            <contrast value>[term]
        Remarks:
            Sets the display contrast for the front panel LCD.
        """
        self.go('BRIGT ' + command)

    def DisplayContrastQuery(self):
        """Display Contrast Query
        Input:
        BRIGT? [term]
        Returned:
        <contrast value>[term]
        Format:
        nn (refer to command for description)
        """
        return self.go('BRIGT?')

    def CelsiusReadingQuery(self, command):
        """Celsius Reading Query
        Input:
            CRDG? <input>[term]
        Format:
            a
            <input> Specifies input to query: A-D (D1–D5 for 3062 option)
        Returned:
            <temp value>
            Or if all inputs are queried: <A value>,<B value>,<C value>,<D value>
        Format:
            ±nnnnnnn[term]
            Or if all inputs are queried: ±nnnnn,±nnnnn,±nnnnn,±nnnnn[term]
        Remarks:
            Returns the Celsius reading for a single input or all inputs.
            <input> specifies which input(s) to query. 0 = all inputs.Also see the RDGST? command.
            """
        return self.go('CRDG? ' + command)

    def CurveDeleteCommand(self, command):
        """Curve Delete Command
        Input:
            CRVDEL <curve>[term]
        Format:
            nn
            <curve> Specifies a user curve to delete. Vaild entries 21-59.
        Example:
            CR  VDEL 21[term] — deletes User Curve 21.
        """
        self.go('CRVDEL ' + command)

    def CurveHeaderCommand(self, command):
        """Curve Header Command
        Input:
            CRVHDR <curve>,<name>,<SN>,<format>,<limit value>,<coefficient>[term]
        Format:
            nn,s[15],s[10],n,+nnn.nnn,n
            <curve> Specifies which curve to configure. Valid entries: 21–59.
            <name> Specifies curve name. Limited to 15 characters.
            <SN> Specifies the curve serial number. Limited to 10 characters.
            <format> Specifies the curve data format. Valid entries: 1 = mV/K, 2 = V/K, 3 = Ohm/K, 4 = logOhm/K.
            <limit value> Specifies the curve temperature limit in kelvin.
            <coefficient> Specifies the curves temperature coefficient. Valid entries: 1 = negative, 2 = positive.
        Remarks:
            Configures the user curve header. The coefficient parameter will be calculated auto-
            matically based on the first 2 curve datapoints. It is included as a parameter for com-
            patability with the CRVHDR? query.
        Example:
            CR  VHDR 21,DT-470,00011134,2,325.0,1[term]—configures User Curve 21 with a
            name of DT-470, serial number of 00011134, data format of volts versus kelvin, upper
            temperature limit of 325 K, and negative coefficient.
        """
        self.go('CRVHDR' + command)

    def CurveHeaderQuery(self, command):
        """Curve Header Query
        Input:
            CRVHDR? <curve>[term]
        Format:
            nn
            <curve> Valid entries: 1–59.
        Returned:
            <name>,<SN>,<format>,<limit value>,<coefficient>[term]
        Format:
            s[15],s[10],n,+nnn.nnn,n (refer to command for description)
        """
        string = self.go('CRVHDR?' + command)
        # string to list
        return listofdata

    def CurveDataPointCommand(self, command):
        """Curve Data Point Command
        Input:
            CRVPT <curve>,<index>,<units value>,<temp value>[term]
        Format:
            nn,nnn,±nnnnnn,+nnnnnn
            <curve> Specifies which curve to configure. Valid entries: 21–59.
            <index> Specifies the points index in the curve. Valid entries: 1–200.
            <units value> Specifies sensor units for this point to 6 digits.
            <temp value> Specifies the corresponding temperature in kelvin for this point to 6 digits.
        Remarks:
            Configures a user curve data point.
        Example:
            CRVPT 21,2,0.10191,470.000,N[term] — sets User Curve 21 second data point to 0.10191 sensor units and 470.000 K.    
        """
        self.go('CRVPT ' + command)

    def CurveDataPointQuery(self, command):
        """Curve Data Point Query
        Input:
            CRVPT? <curve>,<index>[term]
        Format:
            nn,nnn
            <curve> Specifies which curve to query: 1–59.
            <index> Specifies the points index in the curve: 1–200.
        Returned: <units value>,<temp value>[term]
        Format:
            ±nnnnnn,+nnnnnn (refer to command for description)
        Remarks:
            Returns a standard or user curve data point.        
        """
        return self.go('CRVPT? ' + command)

    def FactoryDefaultsCommand(self):
        """Factory Defaults Command
        Input:
            DFLT 99[term]
        Remarks:
            Sets all configuration values to factory defaults and resets the instrument.
            The “99” is included to prevent accidentally setting the unit to defaults.
        """
        self.go('DFLT')

    def DiodeExcitationCurrentParameterCommand(self, command):
        """Diode Excitation Current Parameter Command
        Input:
            DIOCUR <input>,<excitation>[term]
        Format:
            a,n
            <input> Specifies which input to configure: D2–D5 (only for the 3062 card).
            <excitatio > Specifies the Diode excitation current: 0 = 10 μA, 1 = 1 mA.
        Remarks:
            The 10 μA excitation current is the only calibrated excitation current, and is used in almost
            all applications. Therefore the Model 350 will default the 10 μA current set- ting any time the input
            sensor type is changed in order to prevent an accidental change. If using a current that is not 10 μA,
            the input sensor type must first be config- ured to Diode (INTYPE command). If the sensor type is not
            set to Diode when the  DIOCUR command is sent, the command will be ignored
        """
        self.go('DIOCUR ' + command)

    def CustomModeDisplayFieldCommand(self, command):
        """Custom Mode Display Field Command
        Input:
            DISPFLD <field>,<input>,<units>[term]
        Format:
            n,n,n
            <field> Specifies field (display location) to configure: 1–8.
            <input> Specifies item to display in the field: 0 = None, 1 = Input A, 2 = InputB, 3 = InputC,
            4 = InputD (5 = InputD2, 6 = InputD3, 7 = Input D4, 8 = Input D5 for 3062 option)
            <units> Valid entries: 1 = kelvin, 2 = Celsius, 3 = sensor units, 4 = minimum data, and 5 = maximum data.
        Examole:
            DISPFLD 2,1,1[term] — displays kelvin reading for Input A in display field 2 when display mode is set to Custom.
        Remarks:
            This command only applies to the readings displayed in the Custom display mode. All other display
            modes have predefined readings in predefined locations, and will use the Preferred Units parameter to
            determine which units to display for each sensor input. Refer to section 4.3 for details on display setup.
        """
        self.go('DISPFLD ' + command)

    def CustomModeDisplayFieldQuery(self, command):
        """Custom Mode Field Query
        Input:
            DISPFLD? <field>[term]
        Format:
            n
            <field> Specifies field (display location) to query: 1–8.
        Returned:
            <input>,<units>[term]
        Format:
            n,n (refer to command for description)
        """
        self.go('DISPFLD? ' + command)

    def DisplaySetupCommand(self, command):
        """Display Setup Command
        Input:
            DISPLAY <mode>,<num fields>,<output source>[term]
        Format:
            n,n,n
            <mode> Specifies display mode: 0 = Input A, 1 = Input B, 2 = Input C, 3 = Input D, 4 = Custom,
            5 = Four Loop, 6 = All Inputs, (7 = Input D2, 8 = Input D3, 9 = Input D4, 10 = Input D5 for 3062 option)
            <num fields> When mode is set to Custom, specifies number of fields (display locations) to display:
            0 = 2 large, 1 = 4 large, 2 = 8 small. When mode is set to All Inputs, specifies size of readings:
            0 = small with input names, 1 = large without input names
            <displayed output> Specifies which output, and associated loop information, to display in the bottom
            half of the custom display screen:
            1 = Output 1, 2 = Output 2,3 = Output 3, 4 = Output 4
        Example:
            DI  SPLAY 4,0,1[term]—set display mode to Custom with 2 large display fields, and set custom output display source to Output 1.
        Remarks:
            The <num fields> and <displayed output> commands are ignored in all display modes except for Custom.        
        """
        self.go('DISPLAY' + command)

    def DisplaySetupQuery(self):
        """Display Setup Query
        Input:
            DISPLAY?[term]
        Returned:
            <mode>,<num fields>,<output source>[term]
        Format:
            n,n,n (refer to command for description)
        """
        return self.go('DISPLAY?')

    def InputFilterParameterCommand(self, command):
        """Input Filter Parameter Command
        Input:
            FILTER <input>,<off/on>,<points>,<window>[term]
        Format:
            a,n,nn,nn
            <input> Specifies input to configure: A - D (D1 - D5 for 3062 option).
            <off/on> Specifies whether the filter function is 0 = Off or 1 = On.
            <points> Specifies how many data points the filtering function uses.  Valid range = 2 to 64.
            <window> Specifies what percent of full scale reading limits the filtering function.
            Reading changes greater than this percentage reset the filter. Valid range = 1 to 10%.
        Example:
            FI  LTER B,1,10,2[term] — filter input B data through 10 readings with 2% of full scale window.
        """
        self.go('FILTER ' + command)

    def InputFilterParameterQuery(self, command):
        """Input Filter Parameter Query
        Input:
            FILTER? <input>[term]
        Format:
            a
            <input> Specifies input to query: A - D (D1 - D5 for 3062 option).
        Returned:
            <off/on >,<points>,<window>[term]
        Format:
            n,nn,nn (refer to command for description)
        """
        return self.go('FILTER?' + command)

    def HeaterOutputQuery(self, command):
        """ Heater Output Query
        Input:
            HTR? <output>[term]
        Format:
            n
            <output> Heater output to query: 1 = Output 1, 2 = Output 2
        Returned
            <heater value>[term]
        Format:
            +nnn.n
            <heater value>Heater output in percent (%).
        Remarks:
            HTR? is for the Heater Outputs, 1 and 2, only. Use AOUT? for Outputs 3 and 4.
        """
        return self.go('HTR? ' + command)

    def HeaterSetupCommand(self, command):
        """Heater Setup Command
        Input: 
            TRSET <output>,<heater resistance>,<max current>,<max usercurrent>,<current/power>[term]
        Format:
            n,n,n,+n.nnn,n
            <output> Specifies which heater output to configure: 1 or 2.
            <htr resistance> Heater Resistance Setting (output 1 only): 1 = 25 Ohm,2 = 50 Ohm.
            <max current> Specifies the maximum heater output current (output 1 only):
            0 = User Specified, 1 = 0.707A, 2 = 1A, 3 = 1.141A, 4 = 2A
            <current/power> Specifies whether the heater output displays in current or power. Valid entries:
            1 = current, 2 = power.
        Example:
            HTRSET 1,1,2,0,1[term] — Heater output 1 will use the 25 Ohm heater setting, has a maximum current
            of 1 A, the maximum user current is set to 0 A because it is not going to be used since a discrete value
            has been chosen, and the heater output will be displayed in units of current.
        """
        self.go('HTRSET ' + command)

    def HeaterSetupQuery(self, command):
        """Heater Setup Query
        Input:
            HTRSET? <output>[term]
        Format:
            n
            <output> Specifies which heater output to query: 1 or 2.
        Returned:
            <htr resistance>,<max current>,<max user current>,<current/power>[term]
        Format:
            n,n,+n.nnn,n
        """
        return self.go('HTRSET? ' + command)

    def HeaterStatusQuery(self, command):
        """Heater Status Query
        Input:
            HTRST? <output>[term]
        Format:
            n
            <output> Specifies which heater output to query: 1 or 2.
        Returned:
            <error code>[term]
        Format:
            n
            <error code> Heater error code: 0 = no error, 1 = heater open load, 2 = heater short for
            output 1, or heater compliance for output 2.
        Remarks:
            Error condition is cleared upon querying the heater status, except for the heater com-
            pliance error for output 2 which does not latch querying the heater status, will also clear the
            front panel error message for heater open or heater short error messages.
        """
        return self.go('HTRST? ' + command)

    def IEEE488InterfaceParameterCommand(self, command):
        """IEEE-488 Interface Parameter Command
        Input:
            IEEE <address>[term]
        Format:
            nn
            <address> Specifies the IEEE address: 1–30. (Address 0 and 31 are reserved.)
        Example:
            IEEE 4[term]—after receipt of the current terminator, the instrument responds to address 4.
        """
        self.go('IEEE ' + command)

    def IEEE488InterfaceQuery(self):
        """IEEE-488 Interface Parameter Query
        Input:
            IEEE?[term]
        Returned:
            <address>[term]
        Format:
            nn (refer to command for description)
        """
        return self.go('IEEE?')

    def InputCurveNumberCommand(self, command):
        """Input Curve Number Command
        Input:
            INCRV <input>,<curve number>[term]
        Format:
            a,nn
            <input> Specifies which input to configure: A - D (D1 - D5 for 3062 option).
            <curvenumber> Specifies which curve the input uses.If specified curve type does not match the
            configured input type, the curve number defaults to 0. Valid entries:
            0 = none, 1–20 = standard curves, 21–59 = user curves
        Remarks:
            Specifies the curve an input uses for temperature conversion.
        Example:
            INCRV A,23[term]—Input A uses User Curve 23 for temperature conversion.
        """
        self.go('INCRV ' + command)

    def InputCurveNumberQuery(self, command):
        """Input Curve Number Query
        Input:
            INCRV? <input>[term]
        Format:
            a
            <input> Specifies which input to query: A - D (D1 - D5 for 3062 option).
        Returned:
            <curve number>[term]
        Format:
            nn (refer to command for description)
        """
        return self.go('INRCV? ' + command)


    def SensorInputNameCommand(self, command):
        """Sensor Input Name Command
        Input:
            INNAME <input>,<name>[term]
        Format:
            a,s[15]
            <input> Specifies input to configure: A - D (D1 - D5 for 3062 option).
            <name> Specifies the name to associate with the sensor input.
        Example:
            INNAME A, “Sample Space”[term]—the string “Sample Space” will appear on the front panel
            display when possible to identify the sensor information being displayed.
        Remarks:
            Be sure to use quotes when sending strings, otherwise characters such as spaces, and other
            non alpha-numeric characters, will be interpreted as a delimiter and the full string will not be accepted.
            It is not recommended to use commas or semi-colons in sensor input names as these characters are used
            as delimiters for query responses.
        """
        self.go('INNAME ' + command)

    def SensorInputNameQuery(self, command):
        """Sensor Input Name Query
        Input:
            INNAME? <input>[term]
        Format:
            a
            <input> Specifies input to query: A - D (D1 - D5 for 3062 option).
        Returned:
            <name>[term]
        Format:
            s[15] (refer to command for description)
        """
        return self.go('INNAME? ' + command)

    def InterfaceSelectCommand(self, command):
        """Interface Select Command
        Input:
            INTSEL <interface>[term]
        Format:
            n
            <interface> Specifies the remote interface to enable: 0 = USB, 1 = Ethernet, 2 = IEEE-488.
        Remarks:
            The Ethernet interface will attempt to configure itself based on the current configu-
            ration parameters, which can be set using the NET command. Configuring the Ether-
            net interface parameters prior to enabling the interface is recommended.
        """
        self.go('INTSEL ' + command)

    def InterfaceSelectQuery(self):
        """Interface Select Query
        Input:
            INTSEL?[term]
        Returned:
            <interface>[term]
        Format:
            n (refer to command for description)
        """
        return self.go('INTSEL?')

    def InputTypeParameterCommand(self, command):
        """Input Type Parameter Command
        Input:
            INTYPE <input>,<sensor type>,<autorange>,<range>,<compensation>,<units>,<sensor excitation> [term]
        Format:
            a,n,n,n,n,n
            <input>             Specifies input to configure: A - D (D1 - D5 for 3062 option)
            <sensor type>       Specifies input sensor type:
                                0 = Disabled, 1 = Diode (3062 option only), 2 = Platinum RTD, 3 = NTCRTD,
                                4 = Thermocouple (3060 option only), 5 = Capacitance (3061 option only)
            <autorange>         Specifies autoranging: 0 = off and 1 = on.
            <range>             Specifies input range when autorange is off:
                                ###Lakeshore350 Manual; Table 6-8 Input range
            <compensation>      Specifies input compensation where 0 = off and 1 = on. Reversal for thermal EMF
                                compensation if input is resistive, room compensation if input is thermocouple. Also used to set
                                temperature coefficient for capacitance sensors where 0 = negative and 1 = positive.
                                Always 0 if input is a diode. (3062 option only)
            <units>             Specifies the preferred units parameter for sensor readings and for the control setpoint: 1 = kelvin, 2 = Celsius, 3 = Sensor
            <sensor excitation> Specifies the sensor excitation voltage level to maintain for the NTCRTDsensortype.0=1mVand1=10mV
        Example:
            INTYPE A,3,1,0,1,1,1[term]—sets Input A sensor type to NTC RTD, autorange on, thermal compensation on, preferred units to kelvin, and sensor excitation to 1 mV.
        Remarks:
            The <autorange> parameter does not apply to diode, thermocouple, or capacitance sensor types, the <range> parameter does not apply to the thermocouple sensor type, the <compensation> parameter does not apply to the diode sensor type, and the <sen- sor excitation> parameter only applies to the NTC RTD sensor type. When configuring sensor inputs, all parameters must be included, but non-applicable parameters are ignored. A setting of 0 for each is recommended in this case.
        """
        self.go('INTYPE ' + command)

    def InputTypeParameterQuery(self, command):
        pass

    def KelvinReadingQuery(self):
        """Kelvin Reading Query
        Input:
            KRDG? <input>[term]
        Format:
            a
            <input> Specifies input to query: A-D (D1–D5 for 3062 option)
        Returned:
            <temp value>
            Or if all inputs are queried:
            <A value>,<B value>,<C value>,<D value>
        Format:
            +nnnnnnn[term]
            Or if all inputs are queried:
            +nnnnn,+nnnnn,+nnnnn,+nnnnn[term]
        Remarks:
            Returns the Kelvin reading for a single input or all inputs. <input> specifies which input(s) to query. 0 = all inputs.
            Also see the RDGST? command.
        """
        self.go('KRDG?')

    def FrontPanelLEDSCommand(self, command):
        """Front Panel LEDS Command
        Input:
            LEDS <off/on>[term]
        Format:
            n
            <off/on> 0 = LEDs Off, 1 = LEDs On
        Remarks:
            If set to 0, front panel LEDs will not be functional. Function can be used when display brightness is a problem.
        Example:
            LED 0[term]—turns all front panel LED functionality off.
        """
        self.go('LEDS ' + command)

    def FrontPanelLEDSQuery(self):
        """Front Panel LEDS Query
        Input:
            LEDS?[term]
        Returned:
            <off/on> [term]
        Format:
            n (refer to command for description)
        """
        return.self.go('LEDS?')


# only docstrings from here

    def FrontPanelKeyboardLockCommand(self, state, code):
        """Front Panel Keyboard Lock Command
        Input:
            LOCK <state>,<code>[term]
        Format:
            n,nnn
            <state>         0 = Unlocked, 1 = Locked
            <code>          Specifies lock-out code. Valid entries are 000 –999.
        Remarks:
            Locks out all front panel entries except pressing the All Off key to immediately turn off all heater outputs. Refer to section 4.7.
        Example:
            LOCK 1,123[term]—enables keypad lock and sets the code to 123.
        """
        pass

    def FrontPanelKeyboardLockQuery(self):
        """Front Panel Keyboard Lock Query
        Input:
            LOCK?[term]
        Returned:
            <state>,<code>[term]
        Format:
            n,nnn (refer to command for description)
        """
        pass

    def MinimumMaximumDataQuery(self):
        """Minimum/Maximum Data Query
        Input:
            MDAT? <input>[term]
        Format:
            a
            <input> Specifies which input to query: A - D (D1 - D5 for 3062 option).
        Returned:
            <min value>,<max value>[term]
        Format:
            ±nnnnnn,±nnnnnn
        Remarks:
            Returns the minimum and maximum input data. Also see the RDGST? command.
        """
        pass

    def MinimumandMaximumFunctionResetCommand(self):
        """Minimum and Maximum Function Reset Command
        Input:
            MNMXRST[term]
        Remarks:
            Resets the minimum and maximum data for all inputs.
        """
        pass

    def RemoteInterfaceModeCommand(self):
        """Remote Interface Mode Command
        Input:
            MODE <mode>[term]
        Format:
            n
            <mode>      0 = local, 1 = remote, 2 = remote with local lockout.
        Example:
            MODE 2[term]—places the Model 350 into remote mode with local lockout.
        """
        pass

    def RemoteInterfaceModeQuery(self):
        """Remote Interface Mode Query
        Input:
            MODE?[term]
        Returned:
            <mode>[term]
        Format:
            n (refer to command for description)
        """
        pass

    def ManualOutputCommand(self):
        """Manual Output Command
        Input:
            MOUT <output>,<value>[term]
        Format:
            n, +nnnnn[term]
            <output>            Specifies output to configure: 1–4.
            <value>             Specifies value for manual output.
        Example:
            MOUT 1,22.45[term]—Output 1 manual output is 22.45%.
        Remarks:
            Manual output only applies to outputs in Closed Loop PID, Zone, or Open Loop modes.
        """
        pass

    def ManualOutputQuery(self):
        """Manual Output Query
        Input:
            MOUT? <output>[term]
        Format:
            n
            <output>            Specifies which output to query: 1 - 4.
        Returned:
            <value>
        Format:
            + nnnnn[term] (refer to command for description)
        """
        pass

    def NetworkSettingsCommand(self):
        """Network Settings Command
        Input:
            NET <DHCP>,<AUTO IP>,<IP>,<Sub Mask>,<Gateway>,<Pri DNS>,<Sec DNS>,<Pref Host>,<Pref Domain>,<Description>[term]
        Format:
            n,n,dd,dd,dd,dd,dd,s[15],s[64],s[32],
            <DHCP>              0 = DHCP off, 1=DHCP on.
            <AUTO IP>           0 = Dynamically configured link-local addressing (Auto IP) off,1=On
            <IP>                IP address for static configuration.
            <Sub Mask>          Subnet mask for static configuration.
            <Gateway>           Gateway address for static configuration.
            <Pri DNS>           Primary DNS address for static configuration.
            <Sec DNS>           Secondary DNS address for static configuration.
            <Pref Host>         Preferred Hostname (15 character maximum)
            <Pref Domain>       Preferred Domain name (64 character maximum)
            <Description>       Instrument description (32 character maximum)
        """
        pass

    def NetworkSettingsQuery(self):
        """Network Settings Query
        Input:
            NET?[term]
        Returned:
            <DHCP>,<AUTO IP>,<IP>,<Sub Mask>,<Gateway>,<Pri DNS>,<Sec DNS>,<Pref Host>,<Pref Domain>,<Description>[term]
        Format:
            n,n,dd,dd,dd,dd,dd,s[15],s[64],s[32] (refer to command for description)
        """
        pass

    def NetworkConfigurationQuery(self):
        """Network Configuration Query
        Input:
            NETID?[term]
        Returned:
            <lan status>,<IP>,<sub mask>,<gateway>,<pri DNS>,<sec DNS>,<mac addr>,<actual host- name>,<actual domain>[term]
        Format:
            n,dd,dd,dd,dd,dd,hh:hh:hh:hh:hh:hh,s[15],s[32]
            <lan status>           Current status of Ethernet connection:   0 = Connected Using Static IP,
                                                                            1 = Connected Using DHCP,
                                                                            2 = Connected Using  Auto IP,
                                                                            3 = Address Not Acquired Error,
                                                                            4 = Duplicate Initial  IP Address Error,
                                                                            5 = Duplicate Ongoing IP Address Error, 
                                                                            6 = Cable Unplugged,
                                                                            7 = Module Error,
                                                                            8 = Acquiring Address,
                                                                            9 = Ethernet Disabled.
                                                                            Refer to section 6.4.2.1 for details on lan status.
            <IP>                    Configured IP address
            <sub mask>              Configured subnet mask
            <gateway>               Configured gateway address
            <pri DNS>               Configured primary DNS address
            <sec DNS>               Configured secondary DNS address
            <actual hostname>       Assigned hostname
            <actual domain>         Assigned domain
            <mac addr>              Module MAC address.
        Remarks:
            This query returns the configured Ethernet parameters. If the Ethernet interface is not configured then IP,
            subnet mask, gateway, primary DNS and secondary DNS parameters will be 0.0.0.0.
        """
        pass

    def OperationalStatusQuery(self):
        """Operational Status Query
        Input:
            OPST? [term]
        Returned:
            <bit weighting> [term]
        Format:
            nnn
        Remarks:
            The integer returned represents the sum of the bit weighting of the operational sta- tus bits. Refer to section 6.2.5.2 for a list of operational status bits.
        """
        pass

    def OperationalStatusEnableCommand(self):
        """
        Input:
            OPSTE <bit weighting> [term]
        Format:
            nnn
        Remarks:
            Each bit has a bit weighting and represents the enable/disable mask of the corre- sponding operational status bit in the Operational Status Register. This determines which status bits can set the corresponding summary bit in the Status Byte Register. To enable a status bit, send the command OPSTE with the sum of the bit weighting for each desired bit. Refer to section 6.2.5.2 for a list of operational status bits.
        """
        pass

    def OperationalStatusEnableQuery(self):
        """Operational Status Enable Query
        Input:
            OPSTE?[term]
        Returned:
            <bit weighting> [term]
        Format:
            nnn (Refer to section 6.2.5.2 for a list of operational status bits)
        """
        pass

    def OperationalStatusRegisterQuery(self):
        """Operational Status Register Query
        Input:
            OPSTR? [term]
        Returned:
            <bit weighting> [term]
        Format:
            nnn
        Remarks:
            The integers returned represent the sum of the bit weighting of the operational sta- tus bits. These status bits are latched when the condition is detected. This register is cleared when it is read. Refer to section 6.2.5.2 for a list of operational status bits.
        """
        pass

    def OutputModeCommand(self):
        """Output Mode Command
        Input:
            OUTMODE <output>,<mode>,<input>,<powerup enable>[term]
        Format:
            n,n,n,n
            <output>                Specifies which output to configure: 1–4.
            <mode>                  Specifies the control mode. Valid entries:  0 = Off,
                                                                                1 = Closed  Loop PID,
                                                                                2 = Zone, 3 = Open Loop,
                                                                                4 = Monitor out, 
                                                                                5 = Warmup Supply
            <input>                 Specifies which input to use for control:   0 = None,
                                                                                1 = A,
                                                                                2 = B,
                                                                                3 = C,
                                                                                4 = D
                                                                                (5 = Input D2,
                                                                                6 = Input D3,
                                                                                7 = Input D4,
                                                                                8 = Input D5 for 3062 option)
            <powerup enable>    Specifies whether the output remains on or shuts off after power cycle.
                                Valid entries:  0 = powerup enable off,
                                                1 = powerup enable on.
        Example:
            OUTMODE 1,2,1,0[term]—Output 1 configured for Zone control mode, using Input A for the control input sensor, and will turn the output off when power is cycled.
        Remarks:
            Modes 4 and 5 are only valid for Analog Outputs (3 and 4).
        """
        pass

    def OutputModeQuery(self):
        """Output Mode Query
        Input:
            OUTMODE? <output>[term]
        Format:
            n
            <output> Specifies which output to query: 1–4.
        Returned:
            <mode>,<input>,<powerup enable>[term]
        Format:
            n,n,n (refer to command for description)
        """
        pass

    def ControlLoopPIDValuesCommand(self):
        """Control Loop PID Values Command
        Input:
            PID <output>,<P value>,<I value>,<D value>[term]
        Format:
            n,+nnnnn,+nnnnn,+nnnn
            <output>            Specifies which output's control loop to configure: 1 - 4.
            <P value>           The value for output Proportional (gain): 0.1 to 1000.
            <I value>           The value for output Integral (reset): 0.1 to 1000.
            <D value>           The value for output Derivative (rate): 0 to 200.
        Remarks:
            Control settings, (P, I, D, and Setpoint) are assigned to outputs, which results in the settings being applied to any loop formed by the output and its control input.
        Example:
            PID 1,10,50,0[term]—Output 1 P is 10, I is 50, and D is 0%.
        """
        pass

    def ControlLoopPIDValuesQuery(self):
        """Control Loop PID Values Query
        Input:
            PID? <output>[term]
        Format:
            n
            <output> Specifies which output’s control loop to query: 1 – 4.
        Returned:
            <P value>,<I value>,<D value>[term]
        Format:
            +nnnnn,+nnnnn,+nnnn (refer to command for description)
        """
        pass

    def ControlSetpointRampParameterCommand(self):
        """Control Setpoint Ramp Parameter Command
        Input:
            RAMP <output>,<off/on>,<rate value>[term]
        Format:
            n,n,nnnn
            <output>            Specifies which output’s control loop to configure: 1 – 4.
            <off/on>            Specifies whether ramping is 0 = Off or 1 = On.
            <rate value>        Specifies setpoint ramp rate in kelvin per minute from 0.001 to 100 K/min.
                                The rate is always positive, but will respond to ramps up or down.
                                A rate of 0 is interpreted as infinite, and will therefore respond as if
                                setpoint ramping were off.
        Example:
            RAMP 1,1,10.5[term]—when Output 1 setpoint is changed, ramp the current set- point to the target setpoint at 10.5 K/minute.
        Remarks:
            Control loop settings are assigned to outputs, which results in the settings being applied to
            the control loop formed by the output and its control input.
        """
        pass

    def ControlSetpointRampParameterQuery(self):
        """Control Setpoint Ramp Parameter Query
        Input:
            RAMP? <output>[term]
        Format:
            n
            <output>            Specifies which output’s control loop to query: 1 – 4.
        Returned:
            <off/on>,<rate value>[term]
        Format:
            n,nnnn (refer to command for description)
        """
        pass

    def ControlSetpointRampStatusQuery(self):
        """Control Setpoint Ramp Status Query
        Input:
            RAMPST? <output>[term]
        Format:
            n
            <output>            Specifies which output’s control loop to query: 1 – 4.
        Returned:
            <ramp status>[term]
        Format:
            n
            <ramp status>       0 = Not ramping,
                                1 = Setpoint is ramping.
        """
        pass

    def HeaterRangeCommand(self):
        """Heater Range Command
        Input:
            RANGE <output>,<range>[term]
        Format:
            n,n
            <output>            Specifies which output to configure: 1–4.
            <range>             For outputs 1 and 2:    0 = Off,
                                                        1 = Range 1,
                                                        2 = Range 2,
                                                        3 = Range 3,
                                                        4 = Range 4,
                                                        5 = Range 5
                                For outputs 3 and 4:    0 = Off,
                                                        1 = On
        Remarks:
            The range setting has no effect if an output is in the Off mode, and does not apply to
            an output in Monitor Out mode. An output in Monitor Out mode is always on.
        """
        pass

    def HeaterRangeQuery(self):
        """Heater Range Query
        Input:
            RANGE? <output>[term]
        Format:
            n
            <output>            Specifies which output to query: 1–4.
        Returned:
            range>[term]
        Format:
            n (refer to command for description)
        """
        pass

    def InputReadingStatusQuery(self):
        """Input Reading Status Query
        Input:
            RDGST? <input>[term]
        Format:
            a
            <input>             Specifies which input to query: A - D (D1 - D5 for 3062 option).
        Returned:
            <status bit weighting>[term]
        Format:
            nnn
        Remarks:
            The integer returned represents the sum of the bit weighting of the input status flag bits.
            A “000” response indicates a valid reading is present.
                Bit     Bit Weighting       Status Indicator
                0           1                   invalid reading
                4           16                  temp underrange
                5           32                  temp overrange
                6           64                  sensor units zero
                7           128                 sensor units overrange
            """
        pass

    def RelayControlParameterCommand(self):
        """Relay Control Parameter Command
        Input:
            RELAY <relay number>,<mode>,<input alarm>,<alarm type>[term]
        Format:
            n,n,a,n
            <relay number>          Specifies which relay to configure: 1 or 2.
            <mode>                  Specifies relay mode. 0 = Off, 1 = On, 2 = Alarms.
            <input alarm>           Specifies which input alarm activates the relay when the
                                    relay is in alarm mode: A - D (D1 - D5 for 3062 option).
            <alarm type>            Specifies the input alarm type that activates the relay when
                                    the relay is in alarm mode. 0 = Low alarm, 1 = High Alarm,
                                    2 = Both Alarms.
        Example:
            RELAY 1,2,B,0[term]–relay 1 activates when Input B low alarm activates.
        """
        pass

    def RelayControlParameterQuery(self):
        """Relay Control Parameter Query
        Input:
            RELAY? <relay number>[term]
        Format:
            n
            <relay number>          Specifies which relay to query: 1 or 2.
        Returned:
            <mode>,<input alarm>,<alarm type>[term]
        Format:
            n,a,n (refer to command for description)
        """
        pass

    def RelayStatusQuery(self):
        """Relay Status Query
        Input:
            RELAYST? <relay number>[term]
        Format:
            n
            <relay number>          Specifies which relay to query: 1 or 2.
        Returned:
            <status>[term]
        Format:
            n                       0 = Off, 1 = On.
        """
        pass

    def GeneratSofCalCurveCommand(self):
        """Generate SoftCal Curve Command
        Input:
            SCAL <std>,<dest>,<SN>,<T1 value>,<U1 value>,<T2 value>,<U2 value>,<T3 value>,<U3 value>[term]
        Format:
            n,nn,S[10],+nnnnnn,±nnnnnn,+nnnnnn,±nnnnnn,+nnnnnn,±nnnnnn
            <std>                   Specifies the standard curve from which to generate a SoftCalTM curve. Valid entries: 1, 6, 7.
            <dest>                  Specifies the user curve to store the SoftCalTM curve. Valid entries: 21–59.
            <SN>                    Specifies the curve serial number. Limited to 10 characters.
            <T1 value>              Specifies first temperature point in kelvin.
            <U1 value>              Specifies first sensors units point.
            <T2 value>              Specifies second temperature point in kelvin.
            <U2 value>              Specifies second sensor units point.
            <T3 value>              Specifies third temperature point in kelvin.
            <U3 value>              Specifies third sensor units point.
        Remarks:
            Generates a SoftCalTM curve. Refer to Paragraph 5.3.
        Example:
            SCAL 1,21,1234567890,4.2,1.6260,77.32,1.0205,300.0,0.5189[term]–generates a
            three-point SoftCalTM curve from standard curve 1 and saves it in user curve 21.
        """
        pass

    def ControlSetpointCommand(self):
        """Control Setpoint Command
        Input:
            SETP <output>,<value>[term]
        Format:
            n,±nnnnnn
            <output>                Specifies which output’s control loop to configure: 1–4.
            <value>                 The value for the setpoint (in the preferred units of the control loop sensor).
        Example:
            SETP 1,122.5[term]—Output 1 setpoint is now 122.5 (based on its units).
        Remarks:
            For outputs 3 and 4, setpoint is only valid in Warmup mode. Control settings, that is,
            P, I, D, and Setpoint, are assigned to outputs, which results in the settings being
            applied to the control loop formed by the output and its control input.
        """
        pass

    def ControlSetpointQuery(self):
        """Control Setpoint Query
        Input:
            SETP? <output>[term]
        Format:
            n
            <output>                Specifies which output to query: 1–4.
        Returned:
            <value>[term]
        Format:
            ±nnnnnn (refer to command for description)
        """
        pass

    def SensorUnitsInputReadingQuery(self):
        """Sensor Units Input Reading Query
        Input:
            SRDG? <input>[term]
        Format:
            a
            <input>                 Specifies input to query: A-D (D1–D5 for 3062 option)
        Returned:
            <temp value>
            Or if all inputs are queried:
            <A value>,<B value>,<C value>,<D value>
        Format:
            +nnnnnnn[term]
            Or if all inputs are queried:
            +nnnnn,+nnnnn,+nnnnn,+nnnnn[term]
        Remarks:
            Returns the sensor inputs reading for a single input or all inputs. <input> specifies
            which input(s) to query. 0 = all inputs.
            Also see the RDGST? command.
        """
        pass

    def ThermocoupleJunctionTemperatureQuery(self):
        """Thermocouple Junction Temperature Query
        Input:
            TEMP?[term]
        Returned:
            <junction temperature>[term]
        Format:
            +nnnnn
        Remarks:
            Temperature is in kelvin. This query returns the temperature of the ceramic thermo-
            couple block used in the room temperature compensation calculation
        """
        pass

    def TemperatureLimitCommand(self):
        """Temperature Limit Command
        Input:
            TLIMIT <input>,<limit>[term]
        Format:
            a,+nnnn
            <input>                 Specifies which input to configure: A - D (D1 - D5 for 3062 option).
            <limit>                 The temperature limit in kelvin for which to shut down all 
                                    control outputs when exceeded. A temperature limit of zero 
                                    turns the temperature limit feature off for the given 
                                    sensor input.
        Example:
            TLIMIT B,450[term]—if the temperature of the sensor on Input B exceeds 450 K, all
            control outputs will be turned off.
        Remarks:
            A temperature limit setting of 0 K turns the temperature limit feature off.
        """
        pass

    def TemperatureLimitQuery(self):
        """Temperature Limit Query
        Input:
            TLIMIT? <input>[term]
        Format:
            a
            <input>                 Specifies which input to query: A - D (D1 - D5 for 3062 option).
        Returned:
            <limit>[term]
        Format:
            +nnnn (refer to command for description)
        """
        pass

    def ControlTUninStatusQuery(self):
        """Control Tuning Status Query
        Input:
            TUNEST?[term]
        Returned:
            <tuning status>,<output>,<error status>,<stage status>[term]
        Format:
            n,n,n,nn
            <tuning status>         0 = no active tuning, 1 = active tuning.
            <output>                Heater output of the control loop being tuned (if tuning): 
                                    1=output1,2=output2,3=output3,4=output4
            <error status>          0 = no tuning error, 1 = tuning error
            <stage status>          Specifies the current stage in the Autotune process. 
                                    If tuning error occurred, stage status represents stage 
                                    that failed.
        Remarks:
            If initial conditions are not met when starting the autotune procedure, causing the
            autotuning process to never actually begin, then the error status will be set to 1 and
            the stage status will be stage 00.
        """
        pass

    def WarmupSupplyParameterCommand(self):
        """Warmup Supply Parameter Command
        Input:
            WARMUP <output>,<control>,<percentage>[term]
        Format:
            n,n,+nnn.nn
            <output>                Specifies which analog output to configure: 3 or 4
            <control>               Specifies the type of control used: 0 = Auto Off, 1 = Continuous
            <percentage>            Specifies the percentage of full scale (10 V) Monitor Out 
                                    voltage to apply to turn on the external power supply.
        Example:
            WARMUP 3,1,50[term]—Output 3 will use the Continuous control mode, with a 5 V
            (50%) output voltage for activating the external power supply.
        Remarks:
            The Output Mode parameter and the Control Input parameter must be configured
            using the OUTMODE command.
        """
        pass

    def WarmupSupplyParameterQuery(self):
        """Warmup Supply Parameter Query
        Input:
            WARMUP? <output>[term]
        Format:
            n,+nnn.nn
            <output>                Specifies which analog output to query: 3 or 4.
        Returned:
            <control>,<percentage>[term]
        Format:
            n,+nnn (refer to command for description)
        """
        pass

    def WebsiteLoginParameters(self):
        """Website Login Parameters
        Input:
            WEBLOG <username>,<password>[term]
        Format:
            s[15],s[15]
            <username>              15 character string representing the website username.
            <password>              15 character string representing the website password.
        Example:
            WEBLOG “user”, “pass” —sets the username to user and the password to pass.
        Remarks:
            Strings can be sent with or without quotation marks, but to send a string that con-
            tains spaces, commas, or semi-colons quotation marks must be used to differentiate
            the actual parameter separator.
        """
        pass

    def WebsiteLoginParameterQuery(self):
        """Website Login Parameter Query
        Input:
            WEBLOG?[term]
        Returned:
            <username>,<password>[term]
        Format:
            s[15],s[15] (refer to command for description)
        Remarks:
            Note that all strings returned by the Model 350 will be padded with spaces to main-
            tain a constant number of characters.
        """
        pass

    def ControlLoopZoneTableParameterCommand(self):
        """Control Loop Zone Table Parameter Command
        Input:
            ZONE <output>,<zone>,<upper bound>,<P value>,<I value>,
            <D value>,<mout value>,<range>,<input>,<rate>[term]
        Format:
            n,nn,+nnnnn, +nnnnn,+nnnnn,+nnnn,+nnnnn, n,n, +nnnn [term]
            <output>                Specifies which heater output to configure: 1 – 4.
            <zone>                  Specifies which zone in the table to configure. Valid entries are: 1–10.
            <upper bound>           Specifies the upper Setpoint boundary of this zone in kelvin.
            <P value>               Specifies the P for this zone: 0.1 to 1000.
            <I value>               Specifies the I for this zone: 0.1 to 1000.
            <D value>               Specifies the D for this zone: 0 to 200%.
            <mout value>            Specifies the manual output for this zone: 0 to 100%.
            <range>                 Specifies the heater range for this zone. Valid entries:
                                    0=Off,1=Low,2=Med,3=High.
            <input>                 Specifies the sensor input to use for this zone. 0 = Default 
                                    (Use previously assigned sensor), 1 = Input A, 2 = Input B, 
                                    3=InputC,4=InputD(5=InputD2,6=InputD3,
                                    7 = Input D4, 8 = Input D5 for 3062 option)
            <rate>                  Specifies the ramp rate for this zone: 0.001 to 100 K/min
        Remarks:
            Configures the output zone parameters. Refer to Paragraph 2.9.
        Example:
            ZONE 1,1,25.0,10,20,0,0,2,2,10[term]—Output 1 zone 1 is valid to 25.0 K with 
            P=10,I=20,D=0,a heater range of medium,sensor input B,and aramp rate of 10 K/min.
            """
        pass

    def OutputZoneTableParameterQuery(self):
        """Output Zone Table Parameter Query
        Input:
            ZONE? <output>,<zone>[term]
        Format:
            n,nn
            <output>                Specifies which heater output to query: 1 – 4
            <zone>                  Specifies which zone in the table to query. Valid entries: 1–10.
        Returned:
            < upper boundary>,<P value>,<I value>,<D value>,<mout value>,<range>,<input>,<rate>[term]
        Format:
            +nnnnn,+nnnnn,+nnnnn,+nnnn, +nnnnn,n,n, +nnnn 
            (refer to command for description)
        """
        pass
