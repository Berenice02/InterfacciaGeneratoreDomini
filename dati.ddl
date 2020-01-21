DOMAIN cembre0 {
	TEMPORAL_MODULE temporal_module = [0, 100], 100;

	//State Variables
	COMP_TYPE RenewableResource PositionType(2)

	COMP_TYPE SingletonStateVariable CembreType(Idle(), Assembly())
	{
		VALUE Idle() [1, +INF]
		MEETS {
			Assembly();
		}

		VALUE Assembly() [1, +INF]
		MEETS {
			Idle();
		}
	}

	COMP_TYPE SingletonStateVariable CollaborationModalityType(Independent(), Simultaneous(), Supportive(), Synchronous())
	{
		VALUE Independent() [1, +INF]
		MEETS {
			Simultaneous();
			Supportive();
			Synchronous();
		}

		VALUE Simultaneous() [1, +INF]
		MEETS {
			Independent();
			Supportive();
			Synchronous();
		}

		VALUE Supportive() [1, +INF]
		MEETS {
			Independent();
			Simultaneous();
			Synchronous();
		}

		VALUE Synchronous() [1, +INF]
		MEETS {
			Independent();
			Simultaneous();
			Supportive();
		}
	}

	COMP_TYPE SingletonStateVariable HumanProcessType(Idle(), _Task_manipolazione(location), _Task_spostamento(location, location))
	{
		VALUE Idle() [1, +INF]
		MEETS {
			_Task_manipolazione(?location);
			_Task_spostamento(?from, ?to);
		}

		VALUE _Task_manipolazione(?location) [2, 21]
		MEETS {
			Idle();
		}
		
		VALUE _Task_spostamento(?from, ?to) [6, 30]
		MEETS {
			Idle();
		}
		
	}
	
	COMP_TYPE SingletonStateVariable HumanMovementType(_MovingFromTo(location, location), At(location))
	{
		VALUE At(?location) [1, +INF]
		MEETS {
			_MovingFromTo(?from, ?to);
			?from = ?location;
		}

		VALUE _MovingFromTo(?from, ?to) [3, 20]
		MEETS {
			At(?location);
			?location = ?to;
		}
	}

	COMP_TYPE SingletonStateVariable RoboticProcessType(Idle(), Task_manipolazione(location), Task_spostamento(location, location))
	{
		VALUE Idle() [1, +INF]
		MEETS {
			Task_manipolazione(?location);
			Task_spostamento(?from, ?to);
		}

		VALUE Task_manipolazione(?location) [1, +INF]
		MEETS {
			Idle();
		}
		
		VALUE Task_spostamento(?from, ?to) [1, +INF]
		MEETS {
			Idle();
		}
	}
	
	COMP_TYPE SingletonStateVariable RoboticMovementType(MovingFromTo(location, location), At(location))
	{
		VALUE At(?location) [1, +INF]
		MEETS {
			MovingFromTo(?from, ?to);
			?from = ?location;
		}

		VALUE MovingFromTo(?from, ?to) [1, +INF]
		MEETS {
			At(?location);
			?location = ?to;
		}
	}

	COMP_TYPE SingletonStateVariable RoboticType(Idle(), Manipulating(), Pick(), Place(), Holding())
	{
		VALUE Idle() [1, +INF]
		MEETS {
			Manipulating();
			Pick();
		}

		VALUE Manipulating() [1, +INF]
		MEETS {
			Idle();
		}
		
		VALUE Pick() [1, +INF]
		MEETS {
			Holding();
		}
		
		VALUE Holding() [1, +INF]
		MEETS {
			Place();
		}
		
		VALUE Place() [1, +INF]
		MEETS {
			Idle();
		}
	}

	COMP_TYPE SingletonStateVariable RoboticArmType(Idle(), _Activating(), Handle(), _Deactivating())
	{
		VALUE Idle() [1, +INF]
		MEETS {
			_Activating();
		}

		VALUE _Activating() [1, 5]
		MEETS {
			Handle();
		}

		VALUE Handle() [1, +INF]
		MEETS {
			_Deactivating();
		}

		VALUE _Deactivating() [1, 5]
		MEETS {
			Idle();
		}
	}

	COMP_TYPE SingletonStateVariable RoboticToolType(Closed(), Open())
	{
		VALUE Open() [1, +INF]
		MEETS {
			Closed();
		}

		VALUE Closed() [1, +INF]
		MEETS {
			Open();
		}
	}

	//Components
	COMPONENT Cembre {FLEXIBLE case_study(primitive)}: CembreType;
	COMPONENT AssemblyProcess {FLEXIBLE tasks(primitive)}: AssemblyProcessType;

	// collaboration modality
	COMPONENT CollaborationType {FLEXIBLE modality(primitive)}: CollaborationModalityType;

	// human operator components
	COMPONENT HumanProcess {FLEXIBLE process(primitive)}: HumanProcessType;
	COMPONENT Human {FLEXIBLE motions(primitive)}: HumanMovementType;

	// robot operator components
	COMPONENT RoboticProcess {FLEXIBLE process(primitive)}: RoboticProcessType;
	COMPONENT Robot {FLEXIBLE operator(primitive)}: RoboticType;
	COMPONENT RoboticBase {FLEXIBLE motions(primitive)}: RoboticMovementType;
	COMPONENT Arm {FLEXIBLE arm(primitive)}: RoboticArmType;
	COMPONENT Tool {FLEXIBLE gripper(primitive)}: RoboticToolType;

	//Synchronization Rules
	SYNCHRONIZE HumanProcess.process {
		VALUE _Task_manipolazione(?location) {
			p1 <!> Human.motions.At(?loc1);
			?loc1 = ?location;

			EQUALS p1;
		}
		
		VALUE _Task_spostamento(?from, ?to) {
			p1 <!> Human.motions.At(?loc1);
			?loc1 = ?from;
			p2 <!> Human.motions.At(?loc2);
			?loc2 = ?to;
			
			p1 BEFORE [0, +INF] p2;
			
			CONTAINS [0, +INF] [0, +INF] p1;
			CONTAINS [0, +INF] [0, +INF] p2;
		}
	}

	SYNCHRONIZE RoboticProcess.process {
		VALUE Task_manipolazione(?location) {
			r1 <!> Robot.operator.Manipulating();
			p1 <!> RoboticBase.motions.At(?loc1);
			?loc1 = ?location;

			p1 CONTAINS [0, +INF] [0, +INF] r1;

			CONTAINS [0, +INF] [0, +INF] p1;
		}
		
		VALUE Task_spostamento(?from, ?to) {
			r1 <!> Robot.operator.Pick();
			r2 <!> Robot.operator.Place();
			
			p1 <!> RoboticBase.motions.At(?loc1);
			?loc1 = ?from;
			p2 <!> RoboticBase.motions.At(?loc2);
			?loc2 = ?to;
			
			p1 BEFORE [0, +INF] p2;
			p1 CONTAINS [0, +INF] [0, +INF] r1;
			p2 CONTAINS [0, +INF] [0, +INF] r2;
			
			CONTAINS [0, +INF] [0, +INF] r1;
			CONTAINS [0, +INF] [0, +INF] r2;
			CONTAINS [0, +INF] [0, +INF] p1;
			CONTAINS [0, +INF] [0, +INF] p2;
		}
	}

	SYNCHRONIZE Robot.operator {
		VALUE Manipulating() {
			t1 <!> Arm.arm.Handle();

			CONTAINS [0, +INF] [0, +INF] t1;
		}
		
		VALUE Pick()
		{
			t1 <!> Arm.arm.Handle();
			t2 <!> Tool.gripper.Closed();
		
			t2 STARTS-DURING [0, +INF] [0, +INF] t1;
			
			CONTAINS [0, +INF] [0, +INF] t1;
			ENDS-DURING [0, +INF] [0, +INF] t2;
		}
		
		VALUE Place()
		{
			t1 <!> Arm.arm.Handle();
			t2 <!> Tool.gripper.Open();
			
			t2 STARTS-DURING [0, +INF] [0, +INF] t1;
			
			CONTAINS [0, +INF] [0, +INF] t1;
		}
	}

	SYNCHRONIZE RoboticBase.motions {
		VALUE MovingFromTo(?s, ?d) {
			arm <?> Arm.arm.Idle();
			DURING [0, +INF] [0, +INF] arm;
		}
	}

    /*DA QUI INIZIA IL FILE NUOVO*/

//Enumeration Parameter
	PAR_TYPE EnumerationParameterType location = { Pos0, Pos1, Pos2, Pos3, Pos4, Pos5, base };

// position components
	COMPONENT Pos0{FLEXIBLE position(primitive)}: PositionType;
	COMPONENT Pos1{FLEXIBLE position(primitive)}: PositionType;
	COMPONENT Pos2{FLEXIBLE position(primitive)}: PositionType;
	COMPONENT Pos3{FLEXIBLE position(primitive)}: PositionType;
	COMPONENT Pos4{FLEXIBLE position(primitive)}: PositionType;
	COMPONENT Pos5{FLEXIBLE position(primitive)}: PositionType;

	COMP_TYPE SingletonStateVariable AssemblyProcessType(Idle(), T1(), T2())
	{
		VALUE Idle() [1, +INF]
		MEETS {
			T1();
			T2();
		}

		VALUE T1() [1, +INF]
		MEETS {
			Idle();
		}

		VALUE T2() [1, +INF]
		MEETS {
			Idle();
		}

	}

	SYNCHRONIZE Cembre.case_study {
		VALUE Assembly() {
			task0 <!> AssemblyProcess.tasks.T1();
			CONTAINS [0, +INF] [0, +INF] task0;

			task1 <!> AssemblyProcess.tasks.T2();
			CONTAINS [0, +INF] [0, +INF] task1;

			task0 BEFORE [0, +INF] task1;
		}
	}

	SYNCHRONIZE AssemblyProcess.tasks {
		VALUE T1() {
			h0 <!> HumanProcess.process._Task_manipolazione(?hloc0);
			?hloc0 = Pos1;
				hp0 <!> Pos1.position.REQUIREMENT(?amountH0);
				?amountH0 = 1;
				hp0 EQUALS h0;
			r0 <!> RoboticProcess.process.Task_manipolazione(?rloc0);
			?rloc0 = Pos1;
				rp0 <!> Pos1.position.REQUIREMENT(?amountR0);
				?amountR0 = 1;
				rp0 EQUALS r0;

			m CollaborationType.modality.Supportive();
			h0 EQUALS r0;
			m CONTAINS [0, +INF] [0, +INF] h0;
			m CONTAINS [0, +INF] [0, +INF] r0;
			CONTAINS [0, +INF] [0, +INF] h0;
			CONTAINS [0, +INF] [0, +INF] r0;
		}
		VALUE T2() {
			t0 <!> RoboticProcess.process.Task_spostamento(?from0?to<built-in function id>);
			?from0 = Pos1;
			?to0 = Pos3;
				s0 <!> Pos1.position.REQUIREMENT(?amountS0);
				?amountS0 = 2;
				s0 EQUALS t0;
				d0 <!> Pos1.position.REQUIREMENT(?amountD0);
				?amountD0 = 2;
				d0 EQUALS t0;

			m CollaborationType.modality.Independent();
			m CONTAINS [0, +INF] [0, +INF] t0;
			CONTAINS [0, +INF] [0, +INF] t0;
		}
	}

}