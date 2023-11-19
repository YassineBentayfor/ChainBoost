// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ChainBoostCrowdfunding {
    struct Project {
        address creator;
        string title;
        string description;
        uint256 fundingGoal;
        uint256 currentAmount;
        uint256 deadline;
        bool isFunded;
    }

    mapping(uint256 => Project) public projects;
    uint256 public projectsCount;

    event ProjectCreated(uint256 projectId, string title, uint256 fundingGoal, uint256 deadline);
    event ContributionMade(uint256 projectId, address contributor, uint256 amount);

    function createProject(string memory _title, string memory _description, uint256 _fundingGoal, uint256 _durationDays) external {
        require(_fundingGoal > 0, "Funding goal must be greater than zero");

        uint256 deadline = block.timestamp + (_durationDays * 1 days);

        projects[projectsCount] = Project({
            creator: msg.sender,
            title: _title,
            description: _description,
            fundingGoal: _fundingGoal,
            currentAmount: 0,
            deadline: deadline,
            isFunded: false
        });

        emit ProjectCreated(projectsCount, _title, _fundingGoal, deadline);
        projectsCount++;
    }

    function contribute(uint256 _projectId) external payable {
        require(_projectId < projectsCount, "Invalid project ID");
        require(msg.value > 0, "Contribution must be greater than zero");

        Project storage project = projects[_projectId];
        require(!project.isFunded && block.timestamp < project.deadline, "Project funding is closed");

        project.currentAmount += msg.value;

        if (project.currentAmount >= project.fundingGoal) {
            project.isFunded = true;
        }

        emit ContributionMade(_projectId, msg.sender, msg.value);
    }
}
